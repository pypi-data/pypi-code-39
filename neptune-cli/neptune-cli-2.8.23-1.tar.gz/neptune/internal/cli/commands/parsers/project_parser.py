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

from future.builtins import str

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.parsers.abstract_neptune_command_parser import AbstractNeptuneCommandParser
from neptune.internal.cli.commands.parsers.utils.validators import (
    CheckPositionalParamsFirst,
    CombinedArgumentsValidator
)


class ProjectParser(AbstractNeptuneCommandParser):

    def __init__(self, parent):
        super(ProjectParser, self).__init__(parent)
        self.subparsers = self.argparse_parser.add_subparsers(title='Subcommands', dest="subcommand")
        # Required for Python 3.
        # http://bugs.python.org/issue9253#msg186387
        self.subparsers.required = True
        self.activate_parser = ProjectActivateParser(parent=self)

    @staticmethod
    def command_name():
        return CommandNames.PROJECT

    def help(self):
        return u'You can manipulate projects using this command family.'

    def get_validator(self):
        return CombinedArgumentsValidator([CheckPositionalParamsFirst()])


class ProjectActivateParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.ACTIVATE

    def help(self):
        return (u'This command changes the global configuration of your `neptune` command\n'
                u'to use another project by default. This can still be overridden by using\n'
                u'the `--project` option in most commands.\n')

    def _config_positional_args(self):
        self.add_argument(
            name='project',
            type=str,
            help='Name of the project to activate.\n'
                 'It can be either `your-organization/your-project` or simply `your-project`. '
                 'In the latter form, `your-project` is expected to reside within the organization '
                 'associated with your account. If your username is `jacob`, then `jacob/sandbox` points '
                 'to the `sandbox` project within your organization.'
        )
