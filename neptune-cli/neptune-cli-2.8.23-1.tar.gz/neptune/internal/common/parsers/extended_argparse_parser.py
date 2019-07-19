#
# Copyright (c) 2018, deepsense.io
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

import argparse
import sys

from neptune.internal.common.parsers.common_parameters_configurator import CommonParametersConfigurator
from neptune.internal.common.parsers.type_mapper import TypeMapper


class ExtendedArgparseParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):

        self._public_subcommands = kwargs.pop('public_subcommands', None)

        super(ExtendedArgparseParser, self).__init__(*args, **kwargs)
        self.register('type', bool, TypeMapper.to_bool)

    def error(self, message):
        print(u'Error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)

    def _check_value(self, action, value):
        if action.choices is not None and value not in action.choices:
            possibilities = self._public_subcommands or action.choices
            raise argparse.ArgumentError(
                action, 'invalid choice: {} (choose from [{}])'.format(value, ', '.join(possibilities)))

    def format_help(self):
        """
        This method is required, so that Global Options end up at the end of help.
        Without it, Subcommands are placed after Global Options.
        """

        global_options_list = [
            ag for ag in self._action_groups if ag.title == CommonParametersConfigurator.GLOBAL_OPTIONS_GROUP]

        rest = [ag for ag in self._action_groups if ag.title != CommonParametersConfigurator.GLOBAL_OPTIONS_GROUP]

        self._action_groups = rest + global_options_list

        return super(ExtendedArgparseParser, self).format_help()
