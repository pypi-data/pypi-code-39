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
import abc
import os

from future.builtins import object
from future.utils import with_metaclass

from neptune.internal.common import NeptuneException


class AbstractArgumentsValidator(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def validate(self, arguments, raw_args):
        pass


class ArgumentsValidationException(NeptuneException):
    pass


class CheckPositionalParamsFirst(AbstractArgumentsValidator):

    def validate(self, arguments, raw_args):
        if raw_args[1].startswith('-'):
            raise ArgumentsValidationException(
                u"Invalid arguments: positional parameters must be specified first")


class CombinedArgumentsValidator(AbstractArgumentsValidator):

    def __init__(self, validators):
        self._validators = validators

    def validate(self, arguments, raw_args):
        for validator in self._validators:
            validator.validate(arguments, raw_args)


class VoidValidator(AbstractArgumentsValidator):

    def validate(self, arguments, raw_args):
        pass


class SubcommandValidator(AbstractArgumentsValidator):
    def __init__(self, subcommand_parsers):
        self._subcommand_parsers = subcommand_parsers

    def validate(self, arguments, raw_args):
        subcommand = raw_args[1]
        found_subcommand_parsers = [parser for parser in self._subcommand_parsers]

        if found_subcommand_parsers:
            subcommand_parser = found_subcommand_parsers[0]
            subcommand_parser.get_validator().validate(arguments, raw_args)
        else:
            raise ArgumentsValidationException(u'Unknown subcommand: {}'.format(subcommand))


class PipRequirementsFileValidator(AbstractArgumentsValidator):

    def validate(self, arguments, raw_args):
        pip_requirements_file = getattr(arguments.known_args, 'pip-requirements-file', None)

        if pip_requirements_file:
            pip_requirements_path = os.path.abspath(pip_requirements_file)
            source_path = os.path.abspath(os.path.curdir)

            if not os.path.isfile(pip_requirements_path):
                raise ArgumentsValidationException(
                    u"pip requirements file '{}' not found.".format(pip_requirements_file))

            elif not os.path.commonprefix([pip_requirements_path, source_path]) == source_path:
                raise ArgumentsValidationException(
                    u"pip requirements file '{}' not in source directory.".format(pip_requirements_file))
