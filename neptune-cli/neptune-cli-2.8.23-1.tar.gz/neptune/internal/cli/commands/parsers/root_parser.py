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

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.parsers.account_parser import AccountParser
from neptune.internal.cli.commands.parsers.aliasing import alias
from neptune.internal.cli.commands.parsers.data_parser import DataParser
from neptune.internal.cli.commands.parsers.exec_parser import ExecParser
from neptune.internal.cli.commands.parsers.experiment.run_parser import RunParser
from neptune.internal.cli.commands.parsers.experiment.send_parser import SendParser
from neptune.internal.cli.commands.parsers.experiment_parser import ExperimentParser
from neptune.internal.cli.commands.parsers.project_parser import ProjectParser
from neptune.internal.cli.commands.parsers.utils.neptune_help_formatters import RawDescriptionOnlyHeaderHelpFormatter
from neptune.internal.cli.commands.parsers.utils.validators import ArgumentsValidationException
from neptune.internal.common import NeptuneException
from neptune.internal.common.parsers.extended_argparse_parser import ExtendedArgparseParser
from neptune.internal.common.parsers.neptune_argparse_wrapper import NeptuneArgparseWrapper


class NeptuneRootCommandParser(NeptuneArgparseWrapper):

    NEWLINE_AND_SPACE = u'\n '
    SPACE_AND_NEWLINE = u' \n'

    DESCRIPTION = NEWLINE_AND_SPACE + u'''
Neptune CLI allows you to manage and run your experiments.

Find more information at https://docs.neptune.ml

Use neptune <command | group of commands> -h for more information,
e.g. neptune experiment run -h

Running Experiments

  neptune run                       Run a new experiment locally.
                                    Alias for `neptune experiment run`.

  neptune send                      Run a new experiment in the cloud.
                                    Alias for `neptune experiment send`.

  neptune experiment run            Run a new experiment locally.
  neptune experiment send           Run a new experiment in the cloud.
  neptune experiment send-notebook  Start a new Jupyter notebook in the cloud.
  neptune experiment abort          Stop an experiment.
  neptune experiment list           List current experiments.

Managing Data in Neptune

  neptune data upload               Upload data to Neptune storage.
  neptune data download             Download data from Neptune storage.
  neptune data ls                   Browse your datasets and results.
  neptune data rm                   Remove data from Neptune storage.

Authentication

  neptune account login             Log into your Neptune account.
  neptune account logout            Log out of your Neptune account.

Project

  neptune project activate          Change active Neptune project.
''' + SPACE_AND_NEWLINE

    def __init__(self):
        public_first_level_parsers = [
            alias(CommandNames.RUN, RunParser),
            alias(CommandNames.SEND, SendParser),
            alias(CommandNames.EX, ExperimentParser),
            ExperimentParser, AccountParser, DataParser, ProjectParser,
        ]
        public_subcommands = [p.command_name() for p in public_first_level_parsers]

        registered_first_level_parsers = public_first_level_parsers + [ExecParser]

        super(NeptuneRootCommandParser, self).__init__(
            argparse_parser=self._base_parser(public_subcommands=public_subcommands))

        self.subparsers = self.argparse_parser.add_subparsers(
            title=u'commands', dest=u'command_to_run', metavar=u'<command or group of commands>', prog='neptune')

        # pylint: disable=unused-argument
        def completer(*args, **kwargs):
            return public_subcommands

        self.subparsers.completer = completer

        # Required for Python 3.
        # http://bugs.python.org/issue9253#msg186387
        self.subparsers.required = True

        self.first_level_command_parsers = [
            parser_constructor(parent=self)
            for parser_constructor in registered_first_level_parsers
        ]

    def validate(self, arguments, raw_args):
        command = arguments.known_args.command_to_run
        found_parsers = [parser for parser in self.first_level_command_parsers if parser.command_name() == command]

        if found_parsers:
            command_parser = found_parsers[0]
            try:
                command_parser.get_validator().validate(arguments, raw_args)
            except ArgumentsValidationException:
                command_parser.argparse_parser.print_usage()
                raise
        else:
            raise NeptuneException(u'Unknown command neptune {}'.format(command))

    @staticmethod
    def _base_parser(public_subcommands):
        return ExtendedArgparseParser(
            public_subcommands=public_subcommands,
            prog=u'neptune',
            formatter_class=RawDescriptionOnlyHeaderHelpFormatter,
            usage=u'neptune',
            description=NeptuneRootCommandParser.DESCRIPTION,
            add_help=False
        )
