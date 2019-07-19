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
from neptune.internal.cli.commands.parsers.abstract_neptune_command_parser import AbstractNeptuneCommandParser


class LsParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.LIST

    def help(self):
        return 'List experiments that are currently running or being prepared.'

    def _config_named_args(self):
        configuration_options = self.get_parser().add_argument_group('Configuration')
        self.common_parameters.add_project_param(configuration_options)
