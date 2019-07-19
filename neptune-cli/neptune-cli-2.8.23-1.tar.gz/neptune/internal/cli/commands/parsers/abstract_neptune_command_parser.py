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
from abc import abstractmethod, ABCMeta

from neptune.internal.cli.commands.parsers.utils.neptune_help_formatters import NeptuneRawDescriptionHelpFormatter
from neptune.internal.cli.commands.parsers.utils.validators import VoidValidator
from neptune.internal.common.parsers.neptune_argparse_wrapper import NeptuneArgparseWrapper


class AbstractNeptuneCommandParser(NeptuneArgparseWrapper):
    __metaclass__ = ABCMeta

    def __init__(self, parent):
        super(AbstractNeptuneCommandParser, self).__init__(
            parent.subparsers.add_parser(**self._get_params()))

    def _get_params(self):
        params = {
            'name': self.command_name(),
            'description': self.description(),
            'add_help': False,
            'formatter_class': NeptuneRawDescriptionHelpFormatter
        }
        if self.help() != argparse.SUPPRESS:
            params['help'] = self.help()
        return params

    def get_validator(self):
        return VoidValidator()

    @staticmethod
    @abstractmethod
    def command_name():
        raise NotImplementedError()

    def description(self):
        return self.help()

    @abstractmethod
    def help(self):
        raise NotImplementedError()
