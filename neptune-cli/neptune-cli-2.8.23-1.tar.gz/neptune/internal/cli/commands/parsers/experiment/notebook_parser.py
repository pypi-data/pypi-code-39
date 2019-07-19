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
import argparse

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.parsers.abstract_neptune_command_parser import AbstractNeptuneCommandParser
from neptune.internal.cli.commands.parsers.utils.validators import PipRequirementsFileValidator
from neptune.internal.common.config.job_config import ConfigKeys


class NotebookParser(AbstractNeptuneCommandParser):

    NOTEBOOK_PARAMETER = '--' + ConfigKeys.NOTEBOOK_FILE

    @staticmethod
    def command_name():
        return CommandNames.SEND_NOTEBOOK

    def description(self):
        return self.help() + u'\n\n'

    def get_validator(self):
        return PipRequirementsFileValidator()

    def help(self):
        return u'Start a new Jupyter notebook in the cloud.'

    def _config_named_args(self):
        essential_options = self.get_parser().add_argument_group('Essential Options')
        self.add_notebook_parameter(essential_options)
        self.common_parameters.add_remote_invocation_arguments(essential_options)
        self.common_parameters.add_environment_argument(essential_options)

        advanced_options = self.get_parser().add_argument_group('Advanced Options')
        self.common_parameters.add_exclude_param(advanced_options)
        self.common_parameters.add_backup_param(advanced_options)
        self.common_parameters.add_pip_requirements_param(advanced_options)

        experiment_options = self.get_parser().add_argument_group('Experiment Characteristics')
        self.common_parameters.add_experiment_configuration_arguments(experiment_options)

        configuration_options = self.get_parser().add_argument_group('Configuration')
        self.common_parameters.add_project_param(configuration_options)
        self.common_parameters.add_open_webbrowser_param(configuration_options)

    @classmethod
    def add_notebook_parameter(cls, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '-f', cls.NOTEBOOK_PARAMETER,
            dest=ConfigKeys.NOTEBOOK_FILE,
            nargs='?',
            help="Location of the notebook file (relative to storage root).\n"
                 "If this option is omitted, an empty notebook will be created."
        )
        group.add_argument(
            ConfigKeys.POSITIONAL_NOTEBOOK,
            nargs='?',
            help=argparse.SUPPRESS
        )
