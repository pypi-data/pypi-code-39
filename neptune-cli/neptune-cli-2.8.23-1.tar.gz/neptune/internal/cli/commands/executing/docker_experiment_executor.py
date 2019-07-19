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

from functools import reduce  # pylint:disable=redefined-builtin
import logging
import os
from tempfile import mkstemp

from neptune.generated.swagger_client import ExperimentState
from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.exceptions.enqueue_exceptions import \
    NeptuneFailedToExecute
from neptune.internal.cli.commands.executing.abstract_experiment_executor import AbstractExperimentExecutor
from neptune.internal.cli.commands.utils.pip_requirements_utils import \
    prepare_docker_mount_options_array, prepare_in_docker_pip_requirements_option
from neptune.internal.common.config.job_config import ConfigKeys
from neptune.internal.common.config.neptune_config import ConfigSingleton
from neptune.internal.common.local_storage.local_storage import LocalStorage
from neptune.internal.common.parsers.common_parameters_configurator import \
    CommonParametersConfigurator
from neptune.internal.common.utils.command_line import split_arguments, with_removed_option
from neptune.internal.common.utils.docker import convert_to_docker
from neptune.internal.common.utils.logging_utils import OnlineNeptuneLogger
from neptune.internal.common.utils.version_utils import cli_major_version


class DockerExperimentExecutor(AbstractExperimentExecutor):
    def __init__(self, api_service, job_spawner, local_storage, config, docker_image, custom_execution_paths=None):
        super(DockerExperimentExecutor, self).__init__(logging.getLogger(__name__), api_service, local_storage)
        self._job_spawner = job_spawner
        self._running_process = None
        self._experiment = None
        self._config = config
        self._custom_execution_paths = custom_execution_paths
        self.docker_image = docker_image
        self._local_storage = local_storage

    def _execute(self, experiment, args):
        self._experiment = experiment

        _, config_file_path = mkstemp(prefix='neptune', suffix='.yaml')

        self._create_log_file()

        docker_run_command = self._prepare_execute_in_docker_command(experiment, args, config_file_path)
        self._logger.info("Spawning docker: {}".format(docker_run_command))

        try:
            self._running_process = self._job_spawner.spawn(docker_run_command)
        except NeptuneFailedToExecute as e:
            self._api_service.mark_experiment_failed(experiment, str(e))
            print(str(e))
            return 1
        exit_code = self._running_process.wait_for_finish()

        if exit_code != 0 and exit_code != self.ABORTED_RETURN_CODE:
            original_experiment = self._api_service.get_experiment(experiment.id)
            completed_experiment_states = [
                ExperimentState.succeeded,
                ExperimentState.failed,
                ExperimentState.aborted,
                ExperimentState.crashed
            ]
            if original_experiment.state not in completed_experiment_states:
                print(u"Process exited with return code {}.".format(exit_code))
                docker_traceback = self._running_process.memorized_stderr()
                self._api_service.mark_experiment_failed(original_experiment, docker_traceback)
        return exit_code

    def abort(self):
        if self._running_process is not None:
            self._running_process.abort()
            print("Program has been aborted during experiment execution. Marking experiment as aborted...")
            self._api_service.mark_experiment_aborted([self._experiment.id], with_retries=False)

    def _prepare_execute_in_docker_command(self, experiment, args, config_file_path):
        neptune_config = ConfigSingleton.get()
        original_exec_command = args.raw_args

        docker_exec_args = self._to_exec_command_with_single_experiment_id(
            original_exec_command[1:], experiment.id)

        docker_exec_args = with_removed_option(docker_exec_args, 'config')

        docker_exec_args = \
            (['--' + ConfigKeys.ML_FRAMEWORK, self._config.ml_framework] if self._config.ml_framework else []) + \
            ['--' + CommonParametersConfigurator.INSIDE_DOCKER_PARAMETER] + \
            ['--' + CommonParametersConfigurator.UMASK_ZERO_PARAMETER] + \
            ['--' + CommonParametersConfigurator.TOKEN_FILE_PARAMETER + "=" + "/tmp/.neptune_tokens/tokens/token"] + \
            ['--' + CommonParametersConfigurator.DESIRED_NEPTUNE_VERSION_PARAMETER + '='
             + cli_major_version()] + \
            docker_exec_args

        docker_exec_args = ['neptune', CommandNames.EXEC] + \
                           ['--config', convert_to_docker(config_file_path)] + \
                           ['--{0}'.format(CommonParametersConfigurator.COPY_SOURCES_PARAMETER), '/source'] + \
                           docker_exec_args + \
                           prepare_in_docker_pip_requirements_option(self._config.pip_requirements_file)

        sources_location = self._sources_location()

        neptune_config.write(config_file_path,
                             ConfigKeys.NEPTUNE_CONFIG + [ConfigKeys.LOG_CHANNELS])

        docker_run_command = ['docker', 'run', '--workdir', '/neptune'] + \
                             split_arguments('-i --rm --sig-proxy=false') + \
        [
            '-v', '{config_file}:{docker_config_file}'.format(
                config_file=config_file_path,
                docker_config_file=convert_to_docker(config_file_path)),
            '-v', '{user_tokens}:{docker_tokens}'.format(
                user_tokens=self._local_storage.tokens_directory.absolute_path,
                docker_tokens=LocalStorage(u'/tmp/.neptune_tokens').tokens_directory.absolute_path),
            '-v', '{experiment_src}:/source:ro'.format(
                experiment_src=sources_location),
            '-v', '{input_location}:/input'.format(
                input_location=sources_location),
            '-v', '{neptune_log_file}:{neptune_log_path_in_docker}'.format(
                neptune_log_file=self._local_neptune_log_file_path(),
                neptune_log_path_in_docker=OnlineNeptuneLogger.ONLINE_EXECUTION_IN_CONTAINER_LOG_FILEPATH),
        ] + prepare_docker_mount_options_array(self._config.pip_requirements_file) + \
            [self.docker_image] + \
            docker_exec_args

        return docker_run_command

    def _sources_location(self):
        if self._custom_execution_paths is None:
            return os.getcwd()
        else:
            return self._custom_execution_paths.sources_location

    def _local_neptune_log_file_path(self):
        return os.path.abspath(
            os.path.join(
                self._sources_location(),
                OnlineNeptuneLogger.local_neptune_log_file_name(self._experiment.id)))

    def _create_log_file(self):
        neptune_log_file = self._local_neptune_log_file_path()
        with open(neptune_log_file, 'a'):
            os.utime(neptune_log_file, None)

    @staticmethod
    def _to_exec_command_with_single_experiment_id(original_exec_command, experiment_id):
        exec_options = CommonParametersConfigurator.EXEC_OPTIONS
        command_without_exec_modes = \
            reduce(with_removed_option, exec_options, original_exec_command)

        if command_without_exec_modes == original_exec_command:
            return command_without_exec_modes
        else:
            return [experiment_id] + command_without_exec_modes[1:]
