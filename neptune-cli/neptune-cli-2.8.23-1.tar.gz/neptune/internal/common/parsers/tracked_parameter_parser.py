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

import re
from collections import namedtuple

from neptune.internal.cli.exceptions.job_config_exceptions import NoReferenceParameterInException
from neptune.internal.common.parsers.tracked_parameter_regexes import \
    (GRID_SEARCH_ARRAY_FIND_BRACES_REGEX,
     SIMPLE_PARAMETER_REGEX,
     GRID_SEARCH_RANGE_REGEX,
     REFERENCE_PARAMETER_REGEX, GRID_SEARCH_ARRAY_FIND_TOKENS_REGEX)


class TrackedParameterParser(object):
    def parse(self, args, job_parameters, print_warnings=False):
        last_param_name = None
        tracked_params = []

        for arg in args:
            if self.is_named_parameter(arg):
                last_param_name = arg[2:]
            elif self.is_tracked_parameter(arg):
                tracked_params += [self.parse_tracked_parameter(arg, last_param_name, job_parameters, print_warnings)]
                last_param_name = None

        return tracked_params

    def is_named_parameter(self, arg):
        return arg[:2] == u'--' and arg[2:].replace(u'-', u'').replace(u'_', u'').isalpha()

    def is_tracked_parameter(self, arg):
        return arg != u'' and arg[0] == u'%' and (len(arg) <= 1 or arg[1] != u'%')

    def parse_tracked_parameter(self, arg, dashed_name, job_parameters, print_warnings):
        next_char = arg[1] if len(arg) >= 2 else None

        if next_char == u'[':
            param = self._parse_grid_search_array(arg, dashed_name)
        elif next_char == u'(':
            param = self._parse_grid_search_range(arg, dashed_name)
        elif next_char == u':' or next_char == u' ' or next_char is None:
            param = self._parse_reference_parameter(arg, dashed_name, job_parameters)
        else:
            param = self._parse_simple_parameter(arg, dashed_name)

        param = self._negotiate_value_of_parameter_between_job_and_sysargs(param, job_parameters, arg, print_warnings)
        return param

    @staticmethod
    def _negotiate_value_of_parameter_between_job_and_sysargs(param, job_parameters, arg, print_warnings):
        parameter_name = param.api_name if param.api_name else param.name
        if parameter_name in job_parameters:
            if param.value and 'value' not in job_parameters[parameter_name]:
                job_parameters[parameter_name]['value'] = param.value
            elif not param.value and ('value' in job_parameters[parameter_name] and
                                      job_parameters[parameter_name]['value'] is not None):
                param.value = job_parameters[parameter_name]['value']
            elif param.value and ('value' in job_parameters[parameter_name] and
                                  job_parameters[parameter_name]['value'] is not None):
                param.value = job_parameters[parameter_name]['value']
                if print_warnings:
                    print(u"Parameter '{param_name}' already has a defined value outside sys.argv"
                          .format(param_name=parameter_name))
            else:
                raise NoReferenceParameterInException(parameter_name, arg)
        return param

    def _parse_reference_parameter(self, arg, dashed_name, job_parameters):
        param_value_match = re.match(
            REFERENCE_PARAMETER_REGEX,
            arg[1:]
        )

        if not param_value_match:
            self._raise_syntax_error(arg)

        api_name = self.process_quotable_parameter_field(param_value_match.group(u'api_name'))
        name = api_name if api_name else dashed_name
        if name not in job_parameters or 'value' not in job_parameters[name]:
            raise NoReferenceParameterInException(name, arg)
        value = job_parameters[name]['value']

        return TrackedParameter(dashed_name, api_name, value)

    def _parse_simple_parameter(self, arg, dashed_name):
        param_value_match = re.match(
            SIMPLE_PARAMETER_REGEX,
            arg[1:]
        )

        if not param_value_match:
            self._raise_syntax_error(arg)

        api_name = self.process_quotable_parameter_field(param_value_match.group(u'api_name'))
        value = self.process_quotable_parameter_field(param_value_match.group(u'value'))

        return TrackedParameter(dashed_name, api_name, value)

    def _parse_grid_search_array(self, arg, dashed_name):
        grid_search_array_contents_match = re.match(
            GRID_SEARCH_ARRAY_FIND_BRACES_REGEX,
            arg[1:]
        )

        if not grid_search_array_contents_match:
            self._raise_syntax_error(arg)

        tokens_separated_by_commas = grid_search_array_contents_match.group(u'value')
        tokens = [
            self.process_quotable_parameter_field(quotable_token)
            for quotable_token in re.findall(GRID_SEARCH_ARRAY_FIND_TOKENS_REGEX, tokens_separated_by_commas)
        ]

        api_name = self.process_quotable_parameter_field(grid_search_array_contents_match.group(u'api_name'))
        value = GridSearchArray(values=tokens)

        return TrackedParameter(dashed_name, api_name, value)

    def _parse_grid_search_range(self, arg, dashed_name):
        grid_search_range_match = re.match(
            GRID_SEARCH_RANGE_REGEX,
            arg[1:]
        )

        if not grid_search_range_match:
            self._raise_syntax_error(arg)

        api_name = self.process_quotable_parameter_field(grid_search_range_match.group(u'api_name'))
        value = GridSearchRange(
            start=grid_search_range_match.group('from'),
            end=grid_search_range_match.group('to'),
            step=grid_search_range_match.group('step')
        )

        return TrackedParameter(dashed_name, api_name, value)

    @staticmethod
    def process_quotable_parameter_field(s):
        if s is not None and s.startswith(u'"') and s.endswith(u'"'):
            return s.replace(u'""', u'"')[1:-1]
        else:
            return s

    def _raise_syntax_error(self, arg):
        raise ValueError(
            u'Incorrect parameter syntax "{}"'.format(arg)
        )


TrackedParameterLocationInString = namedtuple(
    u'TrackedParameterLocationInString',
    [u'percent_index', u'colon_index', u'last_char_index']
)


class TrackedParameter(object):
    def __init__(self, name=None, api_name=None, value=None):
        self.name = name
        self.api_name = api_name
        self.value = value

    def display_name(self):
        return self.api_name or self.name

    def __repr__(self):
        return 'TrackedParameter(name=%r,api_name=%r,value=%r)' %\
               (self.name, self.api_name, self.value)

    def __eq__(self, other):
        return isinstance(other, TrackedParameter) and self.name == other.name and self.api_name == other.api_name \
               and self.value == other.value


GridSearchRange = namedtuple(
    u'GridSearchRange',
    [u'start', u'end', u'step']
)

GridSearchArray = namedtuple(
    u'GridSearchArray',
    [u'values']
)


def is_tracked_parameter_gridable(param):
    return isinstance(param.value, GridSearchArray) or isinstance(param.value, GridSearchRange)
