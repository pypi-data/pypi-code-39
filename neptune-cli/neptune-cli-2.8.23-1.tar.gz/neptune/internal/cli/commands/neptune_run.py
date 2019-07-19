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

import json
import os
import sys

from neptune.generated.swagger_client import (InputPath, QueuedRemoteExperimentParams, StringParam)
from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.enqueue_utils import EnqueueUtils
from neptune.internal.cli.commands.executing.execution_paths import ExecutionPaths
from neptune.internal.cli.commands.neptune_command import NeptuneCommand
from neptune.internal.cli.commands.parsers.root_parser import NeptuneRootCommandParser
from neptune.internal.cli.commands.utils.pip_requirements_utils import create_string_param
from neptune.internal.cli.experiments.experiment_creator import ExperimentsCreator
from neptune.internal.cli.storage.populate_storage_utils import (CopyProgressBar, collect_files)
from neptune.internal.cli.storage.upload_storage_utils import upload_to_storage
from neptune.internal.common import NeptuneException
from neptune.internal.common.config.job_config import ConfigKeys
from neptune.internal.common.config.neptune_config import NeptuneConfig, load_global_config, load_local_config
from neptune.internal.common.models.rich_project import ProjectResolver
from neptune.internal.common.parsers.command_parsing_utils import (compose_string_command)
from neptune.internal.common.parsers.common_parameters_configurator import \
    CommonParametersConfigurator
from neptune.internal.common.utils.git import send_git_info_if_present


class NeptuneRun(NeptuneCommand):

    def __init__(self,
                 config,
                 local_storage,
                 api_service,
                 tracked_parameter_parser,
                 web_browser,
                 project,
                 neptune_exec_factory,
                 name,
                 environment=None,
                 inputs=None):

        super(NeptuneRun, self).__init__(name, config, api_service)

        self._tracked_parameter_parser = tracked_parameter_parser
        self._rest_api_url = self.config.rest_url

        self.logger.debug("Rest API url: %s", self._rest_api_url)
        self.project = project
        self.enqueue_utils = EnqueueUtils(config, api_service, web_browser)

        self._neptune_exec_factory = neptune_exec_factory
        self._local_storage = local_storage

        self._command_parser = NeptuneRootCommandParser()
        self.environment = environment
        self.inputs = inputs or []

        self.current_command = None
        self.experiment_ids = []
        self.tracked_params = None
        self.experiment_config = None

        self._experiments_creator = ExperimentsCreator(enqueue_utils=self.enqueue_utils, project=self.project)

    def prepare(self, args):
        self.experiment_config = self._create_run_parameters(args)
        self.tracked_params = \
            self.enqueue_utils.parse_experiment_arguments(self.experiment_config, self._tracked_parameter_parser)
        self.config.parameters = self.experiment_config.parameters

    # pylint:disable=arguments-differ
    def run(self, args):
        try:
            self._ensure_executable_exists()
            self.prepare(args)

            result = self._create_experiments(args)
            self.experiment_ids = result.experiment_ids

            if args.known_args.snapshot:
                custom_execution_paths = self._make_code_snapshot(result.short_id)
                print(self._snapshot_info_message(snapshot_path=custom_execution_paths.sources_location))
            else:
                custom_execution_paths = None

            self._close_experiment_creation_message()

            self._configure_experiments(self.experiment_ids)

            self.exit_code = self._exec_experiments(
                experiment_ids=self.experiment_ids, debug=args.known_args.debug,
                custom_execution_paths=custom_execution_paths)
        except:
            self.exit_code = self.UNKNOWN_EXCEPTION_EXIT_CODE
            raise

    def _create_experiments(self, args):
        return self._experiments_creator.create(
            experiment_config=self.experiment_config, enqueue_command=self._enqueue_command(args.raw_args),
            notebook_absolute_path=self._get_notebook_absolute_path(), tracked_params=self.tracked_params,
            parameters=self.config.parameters, remote_params=self._get_remote_params()
        )

    def _configure_experiments(self, experiment_ids):
        self.api_service.add_experiments_backups(experiment_ids=experiment_ids, globs=list(self.config.backup))
        self._upload_sources(experiment_ids)
        send_git_info_if_present(self.api_service, experiment_ids)

        for experiment_id in experiment_ids:
            self.api_service.mark_experiment_waiting(experiment_id)

    @classmethod
    def _create_run_parameters(cls, args):
        if getattr(args.known_args, 'executable', None):
            print(u"Using --executable is deprecated. Pass the executable as a positional parameter.")
        profile = getattr(args.known_args,
                          ConfigKeys.PROFILE,
                          CommonParametersConfigurator.DEFAULT_PROFILE)

        return NeptuneConfig(
            commandline_args=args,
            local_config=load_local_config(args.known_args.config),
            global_config=load_global_config(profile),
            cli_parameters=(args.known_args.parameter or [])
        )

    def _ensure_executable_exists(self):
        if self.config.executable is None:
            raise NeptuneException(self.config.NO_EXECUTABLE_MESSAGE)

    def _upload_sources(self, experiment_ids):
        files_list, data_size, empty_dir_list = collect_files(exclude=self.config.exclude)
        empty_dir_list = [(x, y.replace("./", "", 1)) for x, y in empty_dir_list]

        copy_progress_bar = CopyProgressBar(data_size, u"Sending sources to server")

        experiment_id = experiment_ids[0]
        upload_to_storage(files_list=files_list,
                          dir_list=empty_dir_list,
                          upload_api_fun=self.api_service.upload_experiment_source,
                          upload_tarstream_api_fun=self.api_service.upload_experiment_source_as_tarstream,
                          callback=copy_progress_bar.update,
                          experiment_id=experiment_id)

        copy_progress_bar.finalize()
        self.api_service.finalize_experiment_upload(
            experiment_id=experiment_id,
            target_experiment_ids=experiment_ids
        )

    def abort(self):
        try:
            if self.current_command is not None:
                self.current_command.abort()
        finally:
            if self.experiment_ids:
                print(u'Marking experiments as aborted...')
                # TODO group abort
                self.api_service.mark_experiment_aborted(self.experiment_ids, with_retries=False)

    @staticmethod
    def _close_experiment_creation_message():
        # Until this call, we can print formatted lines, like this:
        # >
        # > Experiment enqueued, id: ...
        # >
        sys.stdout.write(u'\n')

    @staticmethod
    def _confirmation_message(experiment_id):
        return (u'>\n'
                u'> Started experiment execution, id: {experiment_id}\n'
                u'>\n').format(experiment_id=experiment_id)

    @staticmethod
    def _snapshot_info_message(snapshot_path):
        return (u"> Source code and output are located in: {}\n"
                u">").format(snapshot_path)

    def _make_code_snapshot(self, short_id):
        code_snapshot = self._local_storage.experiments_directory.copy_to_subdir(
            src=os.getcwd(), dst_subdir_name=short_id)
        return ExecutionPaths(sources_location=code_snapshot.absolute_path)

    def _exec_experiments(self, experiment_ids, debug, custom_execution_paths):
        exit_codes = [
            self._exec_experiment(
                experiment_id=experiment_id, print_confirmation=len(experiment_ids) > 1,
                debug=debug, custom_execution_paths=custom_execution_paths)
            for experiment_id in experiment_ids
        ]
        return self._combined_exit_code(exit_codes)

    def _exec_experiment(self, experiment_id, print_confirmation=False, debug=False, custom_execution_paths=None):
        if print_confirmation:
            print(self._confirmation_message(experiment_id))

        exec_args_list = [CommandNames.EXEC, experiment_id]

        CommonParametersConfigurator.append_debug_param(exec_args_list, debug)
        args = self._command_parser.get_arguments(exec_args_list)

        self.current_command = self._neptune_exec_factory.create(
            experiment_id=experiment_id,
            environment=self.environment,
            custom_execution_paths=custom_execution_paths
        )

        self.current_command.run(args)

        return self.current_command.exit_code

    @staticmethod
    def _enqueue_command(raw_args):
        return compose_string_command(raw_args=[u'neptune'] + raw_args)

    def _get_notebook_absolute_path(self):
        return None

    def _get_remote_params(self):
        return None

    @staticmethod
    def _combined_exit_code(exit_codes):
        non_zero_exit_codes = [c for c in exit_codes if c != 0]
        return (non_zero_exit_codes + [0])[0]


class NeptuneRunWorker(NeptuneRun):
    def __init__(self,
                 config,
                 local_storage,
                 api_service,
                 tracked_parameter_parser,
                 inputs,
                 environment,
                 worker,
                 web_browser,
                 project,
                 experiment_executor_factory):

        super(NeptuneRunWorker, self).__init__(config=config, local_storage=local_storage, api_service=api_service,
                                               tracked_parameter_parser=tracked_parameter_parser,
                                               environment=environment, web_browser=web_browser,
                                               project=project, inputs=inputs,
                                               neptune_exec_factory=None, name=CommandNames.SEND)

        self._rest_api_url = self.config.rest_url

        self.logger.debug("Rest API url: %s", self._rest_api_url)
        self.worker = worker
        self.experiment_executor_factory = experiment_executor_factory

    def run(self, args):
        self._ensure_executable_exists()
        self.prepare(args)

        self.experiment_ids = self._create_experiments(args).experiment_ids
        self._close_experiment_creation_message()

        self._configure_experiments(self.experiment_ids)

    def _get_remote_params(self):
        inputs = self._get_inputs()
        string_params = self._get_string_params()
        token = self._get_token()

        return QueuedRemoteExperimentParams(inputs=inputs,
                                            environment=self.environment,
                                            worker_type=self.worker,
                                            string_params=string_params,
                                            token=json.dumps(token, sort_keys=True))

    def _get_string_params(self):
        string_params = []

        ml_framework = self.config.ml_framework
        log_channels = self.config.log_channels
        pip_requirements_file = self.config.pip_requirements_file

        for log_channel in log_channels:
            string_params.append(StringParam(name=CommonParametersConfigurator.LOG_CHANNEL, value=str(log_channel)))
        if ml_framework:
            string_params.append(StringParam(name=ConfigKeys.ML_FRAMEWORK, value=ml_framework))
        if pip_requirements_file:
            string_params.append(create_string_param(pip_requirements_file))

        return string_params

    def _get_token(self):
        offline_token = self.experiment_executor_factory.offline_token_storage_service.load()
        keycloak_api_service = self.experiment_executor_factory.keycloak_api_service
        return keycloak_api_service.request_token_refresh(offline_token.refresh_token).raw

    def _get_inputs(self):
        inputs = []
        for entry in self.inputs:
            split_list = entry.split(':', 1)
            destination = split_list[1] if len(split_list) == 2 else ''
            inputs.append(InputPath(source=split_list[0], destination=destination))

        return inputs


class NeptuneRunFactory(object):

    def __init__(self, api_service, config, local_storage, tracked_parameter_parser, web_browser,
                 experiment_executor_factory):
        self.api_service = api_service
        self.config = config
        self.local_storage = local_storage
        self.tracked_parameter_parser = tracked_parameter_parser
        self.web_browser = web_browser
        self.experiment_executor_factory = experiment_executor_factory

    def create(self, is_local, neptune_exec_factory, environment=None, worker=None, inputs=None):
        web_browser = self.web_browser

        project = ProjectResolver.resolve(
            api_service=self.api_service,
            organization_name=self.config.organization_name,
            project_name=self.config.project_name)

        if is_local:
            return NeptuneRun(
                config=self.config,
                local_storage=self.local_storage,
                api_service=self.api_service,
                tracked_parameter_parser=self.tracked_parameter_parser,
                environment=environment,
                web_browser=web_browser,
                neptune_exec_factory=neptune_exec_factory,
                project=project,
                name=CommandNames.RUN
            )
        else:
            return NeptuneRunWorker(
                config=self.config,
                local_storage=self.local_storage,
                api_service=self.api_service,
                tracked_parameter_parser=self.tracked_parameter_parser,
                inputs=inputs,
                environment=environment,
                worker=worker,
                web_browser=web_browser,
                project=project,
                experiment_executor_factory=self.experiment_executor_factory
            )
