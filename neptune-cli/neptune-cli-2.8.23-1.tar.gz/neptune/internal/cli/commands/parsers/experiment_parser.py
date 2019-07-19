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

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.parsers.abstract_neptune_command_parser import AbstractNeptuneCommandParser
from neptune.internal.cli.commands.parsers.experiment.abort_parser import AbortParser
from neptune.internal.cli.commands.parsers.experiment.ls_parser import LsParser
from neptune.internal.cli.commands.parsers.experiment.notebook_parser import NotebookParser
from neptune.internal.cli.commands.parsers.experiment.run_parser import RunParser
from neptune.internal.cli.commands.parsers.experiment.send_parser import SendParser
from neptune.internal.cli.commands.parsers.utils.validators import (
    CombinedArgumentsValidator,
    SubcommandValidator)


class ExperimentParser(AbstractNeptuneCommandParser):

    def __init__(self, parent):
        super(ExperimentParser, self).__init__(parent)
        self.subparsers = self.argparse_parser.add_subparsers(title='Subcommands', dest="subcommand")

        # Required for Python 3.
        # http://bugs.python.org/issue9253#msg186387
        self.subparsers.required = True

        self.abort_parser = AbortParser(parent=self)
        self.notebook_parser = NotebookParser(parent=self)
        self.send_parser = SendParser(parent=self)
        self.run_parser = RunParser(parent=self)
        self.ls_parser = LsParser(parent=self)

    @staticmethod
    def command_name():
        return CommandNames.EXPERIMENT

    def help(self):
        return u'Using this command family you can start, stop and list your experiments .'

    def get_validator(self):
        return CombinedArgumentsValidator([
            SubcommandValidator([
                self.send_parser,
                self.run_parser,
                self.notebook_parser,
                self.abort_parser,
                self.ls_parser
            ])
        ])
