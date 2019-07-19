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
from future.builtins import object
from future.utils import iteritems

import argparse

from neptune.internal.common.parsers.arguments import Arguments
from neptune.internal.common.parsers.common_parameters_configurator import \
    CommonParametersConfigurator
from neptune.internal.common.utils.str import to_unicode


class NeptuneArgparseWrapper(object):
    def __init__(self, argparse_parser):
        self.argparse_parser = argparse_parser
        self.common_parameters = CommonParametersConfigurator(self)
        self.default_values = {}

        self._config_argparse_parser()

    def add_argument(self, name, *args, **kwargs):
        self.default_values[name] = kwargs.get('default')
        self.argparse_parser.add_argument(name, *args, **kwargs)

    def add_argument_group(self, *args, **kwargs):
        argparse_grp = self.argparse_parser.add_argument_group(*args, **kwargs)
        return ArgparseGroupWrapper(self, argparse_grp)

    def add_mutually_exclusive_group(self, *args, **kwargs):
        argparse_grp = self.argparse_parser.add_mutually_exclusive_group(*args, **kwargs)
        return ArgparseGroupWrapper(self, argparse_grp)

    def set_defaults(self, **kwargs):
        self.argparse_parser.set_defaults(**kwargs)

    def get_known_args(self, args):
        parsed_args, _ = self.argparse_parser.parse_known_args(args)
        return UnicodeNamespace(**vars(parsed_args))

    def get_parser(self):
        return self.argparse_parser

    def get_arguments(self, raw_args):
        args, unknown_args = self.argparse_parser.parse_known_args(raw_args)
        if unknown_args:
            msg = 'unrecognized arguments: {}\n'.format(' '.join(unknown_args))
            command = args.command_to_run if hasattr(args, 'command_to_run') else ''
            subcommand = ' ' + args.subcommand if hasattr(args, 'subcommand') else ''
            msg += "Check 'neptune {command} -h' to see possible arguments.".format(command=command+subcommand)
            self.argparse_parser.error(msg)

        return Arguments(
            [to_unicode(arg) for arg in raw_args],
            UnicodeNamespace(**vars(args))
        )

    def _config_argparse_parser(self):
        self._config_positional_args()
        self._config_named_args()
        self.common_parameters.add_global_options()

    def _config_named_args(self):
        pass

    def _config_positional_args(self):
        pass


class UnicodeNamespace(argparse.Namespace):

    def to_dict(self):
        return {to_unicode(key): value for key, value in iteritems(vars(self))}


class ArgparseGroupWrapper(object):
    def __init__(self, parser, argparse_grp):
        self._parser = parser
        self._argparse_grp = argparse_grp

    def add_argument(self, name, *args, **kwargs):
        self._parser.default_values[name] = kwargs.get('default')
        self._argparse_grp.add_argument(name, *args, **kwargs)
