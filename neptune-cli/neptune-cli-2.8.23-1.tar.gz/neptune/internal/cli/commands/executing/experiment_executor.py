# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import collections
import glob
import logging
import os
from os import getcwd
import shutil
import time

from future.builtins import str

from neptune.generated.swagger_client import models
from neptune.internal.cli import MLFramework
from neptune.internal.cli.commands.exceptions.enqueue_exceptions import \
    NeptunePipInstallFailure
from neptune.internal.cli.commands.executing.abstract_experiment_executor import AbstractExperimentExecutor
from neptune.internal.cli.commands.utils.configuration_overriding_utils import \
    ConfigurationOverridingUtils
from neptune.internal.cli.commands.utils.pip_requirements_utils import install_pip_requirements
from neptune.internal.cli.hardware.metrics.service.metric_service_factory import MetricServiceFactory
from neptune.internal.cli.processes import *
from neptune.internal.cli.storage.populate_storage_utils import collect_files
from neptune.internal.cli.storage.upload_storage_utils import upload_to_storage, UploadEntry
from neptune.internal.cli.threads.hardware_metric_reporting_thread import HardwareMetricReportingThread
from neptune.internal.cli.threads.operations_thread import OperationsThread
from neptune.internal.cli.threads.ping_thread import PingThread
from neptune.internal.common.api.api_model_factories import PropertiesApiModelFactory
from neptune.internal.common.datastream import FileChunkStream
from neptune.internal.common.exceptions.base_exceptions import NeptuneException
from neptune.internal.common.parsers.command_parsing_utils import create_args_from_template
from neptune.internal.common.utils.files import create_dir_if_nonexistent, create_empty_file
from neptune.internal.common.utils.logging_utils import OnlineNeptuneLogger
from neptune.internal.common.websockets.reconnecting_websocket_factory import ReconnectingWebsocketFactory

STDOUT_FILENAME = 'stdout'
STDERR_FILENAME = 'stderr'
OUTPUT_PATH = "/output"
BACKUP_PATH = "/backup"
MEMORIZED_STDERR_LINE_COUNT = 100


class ExperimentExecutor(AbstractExperimentExecutor):
    def __init__(
            self,
            config,
            api_service_factory,
            api_service,
            channel_factory,
            job_spawner,
            offline_token_storage_service,
            keycloak_api_service,
            exec_args_formatter,
            sources_dir_to_copy,
            hardware_metrics_gauge_mode,
            local_storage,
            pip_requirements_file=None,
            custom_execution_paths=None
    ):
        super(ExperimentExecutor, self).__init__(logging.getLogger(__name__), api_service, local_storage)

        self._config = config
        self._api_service_factory = api_service_factory
        self._channel_factory = channel_factory
        self._job_spawner = job_spawner
        self._offline_token_storage_service = offline_token_storage_service
        self._keycloak_api_service = keycloak_api_service
        self._exec_args_formatter = exec_args_formatter
        self._hardware_metrics_gauge_mode = hardware_metrics_gauge_mode

        self._memorized_stderr_line_count = MEMORIZED_STDERR_LINE_COUNT
        self._running_process = None

        self._operations_thread = None
        self._ping_thread = None
        self._hardware_metric_reporting_thread = None

        self._experiment = None
        self._pip_requirements_file = pip_requirements_file
        self._sources_dir_to_copy = sources_dir_to_copy
        self._custom_execution_paths = custom_execution_paths

    def _execute(self, experiment, args):
        self._api_service.mark_experiment_initializing(experiment.id)

        self._spawn_job_related_threads(experiment.id)

        self._experiment = experiment
        execution_info = self._api_service.get_execution_info(experiment.id)

        entrypoint = execution_info.source_info.executable
        experiment_paths = self.experiment_paths()

        self._logger.info(
            "\nsources_location: %s"
            "\nentrypoint: %s"
            "\nstdout_log_location: %s"
            "\nstderr_log_location: %s",
            experiment_paths.sources_location,
            entrypoint,
            experiment_paths.stdout_log_location,
            experiment_paths.stderr_log_location
        )

        self._prepare()

        try:
            self._install_requirements()
        except NeptunePipInstallFailure as e:
            self._interrupt_job_related_threads()
            self._api_service.mark_experiment_failed(experiment, str(e))
            print(str(e))
            return 1
        self._update_basic_job_fields(experiment, args)

        exec_args_template_list = create_args_from_template(execution_info.exec_args_template)

        cmdline_parameters = self._exec_args_formatter.format_exec_args_for_cmdline(
            exec_args_template_list,
            experiment.parameters
        )

        try:
            exit_code = self._start_job(experiment.id, entrypoint=entrypoint,
                                        job_arguments=cmdline_parameters,
                                        notebook_data=experiment.notebook_data,
                                        run_command=execution_info.command,
                                        debug=args.known_args.debug)
        except NeptuneException as e:
            self._api_service.mark_experiment_failed(experiment, str(e))
            print(str(e))
            return 1

        self._logger.info(u'Job %s has finished with exit code %d', entrypoint, exit_code)

        if exit_code != self.ABORTED_RETURN_CODE:
            self._mark_experiment_cleaning(experiment)
            self._postprocess(experiment)
            self._mark_experiment_final_status(experiment, exit_code)

        return exit_code

    def abort(self):
        if self._running_process is not None:
            self._running_process.abort()
            print(u"Program has been aborted during experiment execution. Marking experiment as aborted...")
            self._api_service.mark_experiment_aborted([self._experiment.id], with_retries=False)

    def _update_basic_job_fields(self, experiment, args):
        new_swagger_experiment_tags = ConfigurationOverridingUtils.merge_tags(
            experiment.tags,
            args.known_args.tags)

        experiment_properties = ConfigurationOverridingUtils.merge_properties(
            experiment.properties,
            args.known_args.properties)

        new_swagger_experiment_properties = [
            PropertiesApiModelFactory.create_property(neptune_property.key, neptune_property.value)
            for neptune_property in experiment_properties]

        edit_experiment_params = models.EditExperimentParams()
        edit_experiment_params.name = args.known_args.name
        edit_experiment_params.description = args.known_args.description
        edit_experiment_params.tags = new_swagger_experiment_tags
        edit_experiment_params.properties = new_swagger_experiment_properties

        return self._api_service.update_experiment(
            experiment_id=experiment.id,
            edit_experiment_params=edit_experiment_params)

    def experiment_paths(self):
        custom_exec_paths = self._custom_execution_paths
        sources_location = getcwd() if custom_exec_paths is None else custom_exec_paths.sources_location
        output_path = os.path.abspath(os.path.join(sources_location, u'output'))
        return ExperimentPaths(
            sources_location=sources_location,
            output_directory_location=output_path,
            stdout_log_location=os.path.abspath(os.path.join(output_path, u'stdout')),
            stderr_log_location=os.path.abspath(os.path.join(output_path, u'stderr'))
        )

    def _start_job(self, experiment_id, entrypoint, job_arguments, notebook_data, run_command="",
                   redirect_output_to_console=True, debug=False):

        job_process_env = os.environ.copy()
        job_process_env['NEPTUNE_JOB_ID'] = str(experiment_id)

        job_process_env['NEPTUNE_REST_API_URL'] = self._config.rest_url
        job_process_env['NEPTUNE_WS_API_URL'] = self._config.ws_url
        job_process_env['NEPTUNE_USER_PROFILE_PATH'] = self._local_storage.absolute_path

        if debug:
            job_process_env['NEPTUNE_DEBUG'] = 'yes'

        if MLFramework.Keras == self._config.ml_framework:
            job_process_env['NEPTUNE_INTEGRATE_WITH_KERAS'] = 'yes'

        elif MLFramework.Tensorflow == self._config.ml_framework:
            job_process_env['NEPTUNE_INTEGRATE_WITH_TENSORFLOW'] = 'yes'

        experiment_paths = self.experiment_paths()

        self._logger.info("\nentrypoint: %s\nsources_location: %s", entrypoint, experiment_paths.sources_location)

        try:
            create_dir_if_nonexistent(experiment_paths.output_directory_location)
        except OSError:
            print(u'Could not create output directory {}'.format(experiment_paths.output_directory_location))

        try:
            create_empty_file(experiment_paths.stdout_log_location)
            create_empty_file(experiment_paths.stderr_log_location)
        except IOError:
            print(u'Could not create experiment log files')

        if notebook_data is None:
            language = recognize_execution_command(entrypoint)
        else:
            language = ExecutionCommand.JUPYTER_NOTEBOOK

        command = build_process_command(language, entrypoint, job_arguments)

        self._logger.debug("\ncommand: %s", str(command))

        self._running_process = self._job_spawner.spawn(
            command=command,
            cwd=experiment_paths.sources_location,
            env=job_process_env,
            config=self._config,
            channel_factory=self._channel_factory,
            stdout_filepath=experiment_paths.stdout_log_location,
            stderr_filepath=experiment_paths.stderr_log_location,
            memorized_stderr_line_count=self._memorized_stderr_line_count,
            redirect_output_to_console=redirect_output_to_console)

        self._api_service.mark_experiment_running(experiment_id, run_command)

        return_code = self._running_process.wait_for_finish()
        self._interrupt_job_related_threads()

        if self._operations_thread.received_abort_message():
            return_code = self.ABORTED_RETURN_CODE

        return return_code

    def _mark_experiment_cleaning(self, experiment):
        self._api_service.mark_experiment_cleaning(experiment)

    def _mark_experiment_final_status(self, experiment, return_code):
        if return_code == 0:
            self._api_service.mark_experiment_succeeded(experiment)
        elif return_code == self.ABORTED_RETURN_CODE:
            self._api_service.mark_experiment_aborted([experiment.id], with_retries=False)
        else:
            job_traceback = self._running_process.memorized_stderr()
            print(u"Process exited with return code {}.".format(return_code))
            self._api_service.mark_experiment_failed(experiment, job_traceback)

    def _spawn_job_related_threads(self, experiment_id):
        self._spawn_operations_thread(experiment_id)
        self._spawn_ping_thread(experiment_id)
        self._spawn_hardware_metric_reporting_thread(experiment_id)

    def _spawn_operations_thread(self, experiment_id):
        def running_job_getter():
            return self._running_process
        self._operations_thread = OperationsThread(
            experiment_id=experiment_id,
            running_job_getter=running_job_getter,
            websocket_factory=ReconnectingWebsocketFactory(
                base_address=self._config.ws_url,
                experiment_id=experiment_id,
                offline_token_storage_service=self._offline_token_storage_service,
                keycloak_api_service=self._keycloak_api_service,
                local_storage=self._local_storage
            )
        )
        self._operations_thread.start()

    def _spawn_ping_thread(self, experiment_id):
        def running_job_getter():
            return self._running_process
        self._ping_thread = PingThread(self._api_service_factory, experiment_id, running_job_getter)
        self._ping_thread.start()

    def _spawn_hardware_metric_reporting_thread(self, experiment_id):
        metric_service_factory = MetricServiceFactory(
            api_service=self._api_service, api_service_factory=self._api_service_factory, os_environ=os.environ)
        metric_service = metric_service_factory.create(
            gauge_mode=self._hardware_metrics_gauge_mode, experiment_id=experiment_id, reference_timestamp=time.time())

        self._hardware_metric_reporting_thread = HardwareMetricReportingThread(
            metric_service=metric_service,
            metric_sending_interval_seconds=3
        )
        self._hardware_metric_reporting_thread.start()

    def _interrupt_job_related_threads(self):
        if self._operations_thread:
            self._operations_thread.interrupt()
            self._operations_thread.join()
        if self._ping_thread:
            self._ping_thread.interrupt()
            self._ping_thread.join()
        if self._hardware_metric_reporting_thread:
            self._hardware_metric_reporting_thread.interrupt()
            self._hardware_metric_reporting_thread.join()
        if self._channel_factory:
            self._channel_factory.wait_for_threads()

    def _copytree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def _rmtree(self, src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            if os.path.isdir(s):
                shutil.rmtree(s)
            else:
                os.remove(s)

    def _prepare(self):
        if self._sources_dir_to_copy:
            sources_destination = self.experiment_paths().sources_location
            dir_content = os.listdir(sources_destination)
            if dir_content and dir_content != [OnlineNeptuneLogger.ONLINE_EXECUTION_LOG_FILENAME]:
                raise RuntimeError("Working directory is not empty. Content: {0}".format(dir_content))
            self._rmtree(sources_destination)
            self._copytree(self._sources_dir_to_copy, sources_destination)

    def _check_pip_install_result(self, pip_installation_exit_code):
        if pip_installation_exit_code != 0:
            raise NeptunePipInstallFailure(pip_installation_exit_code)

    def _install_requirements(self):
        if self._pip_requirements_file:
            self._check_pip_install_result(install_pip_requirements(self._pip_requirements_file))

    def _postprocess(self, experiment):
        experiment_paths = self.experiment_paths()
        self._upload_output(experiment, experiment_paths.output_directory_location)
        self._upload_std(experiment, experiment_paths.output_directory_location)
        self._make_backups_via_api(experiment)

    def _upload_output(self, experiment, output_location):
        output_location = os.path.abspath(output_location)
        if not os.path.exists(output_location) or not os.listdir(output_location):
            return

        files_list, _, empty_dir_list = collect_files(p=output_location, exclude=('stderr', 'stdout'))
        files_list = [(x, y.replace(output_location, "", 1)) for x, y in files_list]
        empty_dir_list = [(x, y.replace(output_location, "", 1)) for x, y in empty_dir_list]

        upload_to_storage(files_list=files_list,
                          dir_list=empty_dir_list,
                          upload_api_fun=self._api_service.upload_experiment_output,
                          upload_tarstream_api_fun=self._api_service.extract_experiment_output,
                          experiment_id=experiment.id)

    def _upload_std(self, experiment, std_dir):
        stderr_location = os.path.abspath(os.path.join(std_dir, u'stderr'))
        stdout_location = os.path.abspath(os.path.join(std_dir, u'stdout'))

        if os.path.exists(stderr_location):
            self._api_service.upload_experiment_stderr(experiment.id,
                                                       data=FileChunkStream(UploadEntry(stderr_location,
                                                                                        stderr_location)))

        if os.path.exists(stdout_location):
            self._api_service.upload_experiment_stdout(experiment.id,
                                                       data=FileChunkStream(UploadEntry(stdout_location,
                                                                                        stdout_location)))

    def _make_backups_via_api(self, experiment):
        backups = self._api_service.get_experiment_backups(experiment.id)
        output_paths = []
        for path in backups:
            for filename in glob.glob(path):
                output_paths.append(os.path.abspath(filename))

        output_location = "backup"
        output_paths = [(os.path.join(output_location, rel_path), rel_path) for rel_path in
                        output_paths]

        output_paths = [path for path in output_paths if os.access(path[1], os.R_OK)]

        if not output_paths:
            return

        for filename, _ in output_paths:
            self._api_service.upload_experiment_backups(experiment.id,
                                                        data=FileChunkStream(UploadEntry(filename, filename)))


class GCPJobExecutor(ExperimentExecutor):
    def experiment_paths(self):
        return ExperimentPaths(
            sources_location=getcwd(),
            output_directory_location=OUTPUT_PATH,
            stdout_log_location=os.path.join(OUTPUT_PATH, STDOUT_FILENAME),
            stderr_log_location=os.path.join(OUTPUT_PATH, STDERR_FILENAME)
        )

    def _postprocess(self, experiment):
        self._make_backups_via_mounted_storage(experiment)

    def _make_backups_via_mounted_storage(self, experiment):
        def _ignore_when_not_enough_permissions_to_copy(folder, files):
            ignore_list = []
            for f in files:
                full_path = os.path.join(folder, f)
                if full_path == BACKUP_PATH:
                    ignore_list.append(f)
                else:
                    try:
                        if not os.access(full_path, os.R_OK):
                            ignore_list.append(f)
                    except IOError:
                        ignore_list.append(f)

            return ignore_list

        backups = self._api_service.get_experiment_backups(experiment.id)
        for path in backups:
            for filename in glob.glob(path):
                abspath = os.path.abspath(filename)
                dst = BACKUP_PATH + abspath
                if os.path.isdir(abspath):
                    try:
                        shutil.copytree(abspath, dst, ignore=_ignore_when_not_enough_permissions_to_copy)
                    except OSError:
                        pass
                else:
                    try:
                        if os.access(abspath, os.R_OK):
                            if not os.path.exists(os.path.dirname(dst)):
                                try:
                                    os.makedirs(os.path.dirname(dst))
                                except OSError:
                                    pass
                            shutil.copy2(abspath, dst)
                    except OSError:
                        pass


class InDockerJobExecutor(ExperimentExecutor):
    LOGS_PATH = "/logs"

    def _prepare(self):
        super(InDockerJobExecutor, self)._prepare()
        if not os.path.exists(self.LOGS_PATH):
            try:
                os.makedirs(self.LOGS_PATH)
            except Exception:
                pass

    def experiment_paths(self):
        return ExperimentPaths(
            sources_location=getcwd(),
            output_directory_location=OUTPUT_PATH,
            stdout_log_location=os.path.join(OUTPUT_PATH, STDOUT_FILENAME),
            stderr_log_location=os.path.join(OUTPUT_PATH, STDERR_FILENAME)
        )

    def abort(self):
        ''' No need to do anything. Whole Docker gets killed anyway. '''
        pass

    def _postprocess(self, experiment):
        self._upload_output(experiment, OUTPUT_PATH)
        self._upload_std(experiment, self.LOGS_PATH)
        self._make_backups_via_api(experiment)


ExperimentPaths = collections.namedtuple('ExperimentPaths', [
    'sources_location', 'output_directory_location', 'stdout_log_location', 'stderr_log_location'
])
