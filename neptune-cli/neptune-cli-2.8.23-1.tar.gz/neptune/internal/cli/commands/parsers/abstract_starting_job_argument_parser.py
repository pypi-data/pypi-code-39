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

from abc import ABCMeta, abstractmethod

from neptune.internal.cli.commands.parsers.abstract_neptune_command_parser import AbstractNeptuneCommandParser


class AbstractStartingJobArgumentParser(AbstractNeptuneCommandParser):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def command_name():
        raise NotImplementedError()

    @abstractmethod
    def help(self):
        raise NotImplementedError()

    @classmethod
    def add_command_parameters(cls, parser):
        parser.add_argument(
            'entrypoint',
            nargs='?',
            help="Your Python script to run or any other executable (like bash): "
                 "the main entrypoint to your experiment. After the entrypoint, "
                 "you can add any number of arguments that should be passed to your entrypoint.\n"
                 "If no entrypoint is passed, Neptune will try to run `main.py` by default.",
            metavar='ENTRYPOINT [ARG [...]]'
        )
        parser.add_argument(
            'cmd_args',
            nargs=argparse.REMAINDER,
            help=argparse.SUPPRESS,
            metavar='ARG'
        )
