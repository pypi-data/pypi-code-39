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
import functools
import re
from collections import Counter

from past.builtins import basestring

from neptune.internal.common.parsers.tracked_parameter_parser import GridSearchRange, GridSearchArray

_LEADING_WHITESPACES_REGEX = re.compile(r'^\s+.*$')
_TRAILING_WHITESPACES_REGEX = re.compile(r'^.*\s+$')


class TrackedParameterValidationError(ValueError):
    def __init__(self, *args, **kwargs):
        super(TrackedParameterValidationError, self).__init__(*args, **kwargs)


def validate_tracked_parameters(tracked_parameters):
    for tracked_parameter in tracked_parameters:
        validate_tracked_parameter(tracked_parameter)
    _check_display_names_are_not_duplicated(tracked_parameters)
    return tracked_parameters


def validate_tracked_parameter(tracked_parameter):
    _check_name_is_defined(tracked_parameter)
    _check_name_has_no_leading_or_trailing_whitespaces(tracked_parameter)
    _check_value_is_string_or_grid_search_value(tracked_parameter)

    if isinstance(tracked_parameter.value, GridSearchRange):
        _check_grid_search_range(tracked_parameter)
    elif isinstance(tracked_parameter.value, GridSearchArray):
        _check_grid_search_array(tracked_parameter)
    return tracked_parameter


def _check_name_is_defined(tracked_parameter):
    if not tracked_parameter.display_name():
        raise TrackedParameterValidationError(
            u'Parameter with value: "{}" does not have a name!'.format(str(tracked_parameter.value)))


def _check_name_has_no_leading_or_trailing_whitespaces(tracked_parameter):
    if tracked_parameter.name is not None and _contains_leading_or_trailing_whitespaces(tracked_parameter.name):
        raise TrackedParameterValidationError(
            u'Parameter "{}" contains leading or trailing whitespaces!'.format(tracked_parameter.name))
    if tracked_parameter.api_name is not None and _contains_leading_or_trailing_whitespaces(tracked_parameter.api_name):
        raise TrackedParameterValidationError(
            u'Parameter "{}" contains leading or trailing whitespaces!'.format(tracked_parameter.api_name))


def _contains_leading_or_trailing_whitespaces(s):
    return _LEADING_WHITESPACES_REGEX.match(s) or _TRAILING_WHITESPACES_REGEX.match(s)


def _check_value_is_string_or_grid_search_value(tracked_parameter):
    if tracked_parameter.value is None:
        raise TrackedParameterValidationError(u'Parameter "{}" has no value!'.format(tracked_parameter.display_name()))
    allowed_types = [basestring, GridSearchArray, GridSearchRange]
    value_of_allowed_type = functools.reduce(
        lambda x, y: x or y,
        [isinstance(tracked_parameter.value, allowed_type) for allowed_type in allowed_types]
    )
    if not value_of_allowed_type:
        raise TrackedParameterValidationError(
            u'Parameter "{}" has invalid value type ({})!'. \
            format(tracked_parameter.display_name(), type(tracked_parameter.value)))


def _check_grid_search_range(tracked_parameter):
    if float(tracked_parameter.value.start) > float(tracked_parameter.value.end):
        raise TrackedParameterValidationError(
            u'Grid search parameter "{}" contains an invalid range (`from` > `to`)!'. \
            format(tracked_parameter.display_name()))
    if float(tracked_parameter.value.step) <= 0:
        raise TrackedParameterValidationError(
            u'Grid search parameter "{}" contains an invalid range (`step <= 0`)!'. \
            format(tracked_parameter.display_name()))


def _check_grid_search_array(tracked_parameter):
    if not tracked_parameter.value.values:
        raise TrackedParameterValidationError(
            u'Grid search parameter "{}" is empty!'.format(tracked_parameter.display_name())
        )


def _check_display_names_are_not_duplicated(tracked_parameters):
    display_names = [tracked_parameter.display_name() for tracked_parameter in tracked_parameters]
    duplicated_display_names = [
        u'"{}"'.format(display_name)
        for display_name, occurence_count
        in dict(Counter(display_names)).items()
        if occurence_count > 1
    ]

    if duplicated_display_names:
        raise TrackedParameterValidationError(
            u'Duplicated parameter names: {}!'.format(u', '.join(duplicated_display_names))
        )
