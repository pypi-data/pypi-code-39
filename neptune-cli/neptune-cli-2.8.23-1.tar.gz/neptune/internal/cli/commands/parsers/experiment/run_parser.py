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
from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.parsers.abstract_starting_job_argument_parser import \
    AbstractStartingJobArgumentParser
from neptune.internal.cli.commands.parsers.utils.validators import PipRequirementsFileValidator



class RunParser(AbstractStartingJobArgumentParser):
    DESC = u'''
Without any arguments the command assumes that there is a `main.py` file
in the CWD (current working directory).

  neptune run
  neptune experiment run

You can execute any file within your code with:

  neptune run src/train_neural_net.py

You can pass command line arguments to your code after the Python script.

  neptune run src/train_neural_net.py --learning_rate 0.1

Read more about `neptune experiment run` options below to learn how to select
machine learning environment for your experiment, and much more.
'''

    @staticmethod
    def command_name():
        return CommandNames.RUN

    def description(self):
        return self.help() + '\n\n' + self.DESC

    def get_validator(self):
        return PipRequirementsFileValidator()

    def help(self):
        return u'Execute an experiment locally. `neptune run` is an alias for `neptune experiment run`.'

    def _config_named_args(self):
        essential_options = self.get_parser().add_argument_group('Essential Options')
        self.add_command_parameters(essential_options)
        self.common_parameters.add_environment_argument(essential_options)
        self.common_parameters.add_log_channels_parameter(essential_options)
        self.common_parameters.add_ml_framework_parameter(essential_options)

        advanced_options = self.get_parser().add_argument_group('Advanced Options')
        self.common_parameters.add_exclude_param(advanced_options)
        self.common_parameters.add_parameter_arguments(advanced_options)
        self.common_parameters.add_backup_param(advanced_options)
        self.common_parameters.add_pip_requirements_param(advanced_options)
        self.common_parameters.add_snapshot_param(advanced_options)

        _offline_help = (
            "Execute the experiment locally, without connecting to Neptune.\n"
            "\n"
            "This option is useful for early-stage debugging and when you don't "
            "have access to the Internet."
        )
        advanced_options.add_argument('--offline', action='store_true', default=False, help=_offline_help)

        experiment_options = self.get_parser().add_argument_group('Experiment Characteristics')
        self.common_parameters.add_experiment_arguments(experiment_options)

        configuration_options = self.get_parser().add_argument_group('Configuration')
        self.common_parameters.add_project_param(configuration_options)
        self.common_parameters.add_neptune_global_params(configuration_options)
        self.common_parameters.add_disable_stdout_channel_param(configuration_options)
        self.common_parameters.add_disable_stderr_channel_param(configuration_options)
