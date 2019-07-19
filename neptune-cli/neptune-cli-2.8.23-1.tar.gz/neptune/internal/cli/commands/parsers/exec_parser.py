#
# Copyright (c) 2016, deepsense.io
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
import argparse

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.parsers.abstract_neptune_command_parser import AbstractNeptuneCommandParser
from neptune.internal.cli.commands.parsers.utils.validators import (
    AbstractArgumentsValidator,
    ArgumentsValidationException)


class ExecParser(AbstractNeptuneCommandParser):
    @staticmethod
    def command_name():
        return CommandNames.EXEC

    def description(self):
        return self.help() + u'''
You can execute a specific experiment (passing the [experiment_id] argument),

If you use neptune exec providing an experiment_id, you can pass parameter values as additional named
parameters separated from CLI parameters by double dash (--).

Example: neptune exec (...) -- --param 1 --another-param 2
'''

    def help(self):
        return argparse.SUPPRESS

    def get_validator(self):
        return ValidateExecVariants()

    def _config_positional_args(self):
        super(ExecParser, self)._config_positional_args()
        self.common_parameters.add_experiment_id_positional_param()

    def _config_named_args(self):
        essential_options = self.get_parser().add_argument_group('Essential Options')
        self.common_parameters.add_log_channels_parameter(essential_options)
        self.common_parameters.add_ml_framework_parameter(essential_options)
        self.common_parameters.add_environment_argument(essential_options)
        advanced_options = self.get_parser().add_argument_group('Advanced Options')
        experiment_options = self.get_parser().add_argument_group('Experiment Characteristics')
        self.common_parameters.add_experiment_configuration_arguments(experiment_options)
        configuration_options = self.get_parser().add_argument_group('Configuration')
        self.common_parameters.add_disable_stdout_channel_param(configuration_options)
        self.common_parameters.add_disable_stderr_channel_param(configuration_options)
        self.common_parameters.add_neptune_global_params()
        self.common_parameters.add_docker_image_param()
        self.common_parameters.add_inside_docker_param()
        self.common_parameters.add_inside_gcp_param()
        self.common_parameters.add_umask_zero_param()
        self.common_parameters.add_desired_neptune_version_param()
        self.common_parameters.add_pip_requirements_param(advanced_options)
        self.common_parameters.add_copy_sources_param()
        self.common_parameters.add_token_file_param()

class ValidateExecVariants(AbstractArgumentsValidator):
    def validate(self, arguments, raw_args):
        if not arguments.known_args.experiment_id:
            raise ArgumentsValidationException(
                'Incorrect invocation of neptune exec! '
                'EXPERIMENT_ID is required.')
