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
import re


DEFAULT_FORBIDDEN_CHARS = r'\s":()\[\]'
FORBIDDEN_CHARS_IN_GRID_SEARCH_ARRAY = DEFAULT_FORBIDDEN_CHARS + ','


def unquoted_value_regex_part(forbidden_chars):
    return r'[^{}]+'.format(forbidden_chars)


def quoted_value_regex_part():
    return r'"(?:[^"]|"")*"'


def value_regex_part(forbidden_chars_in_unquoted_text):
    return r'(?:{})|(?:{})'.format(
        unquoted_value_regex_part(forbidden_chars_in_unquoted_text),
        quoted_value_regex_part()
    )


def optional_api_name_regex_part(forbidden_chars_in_unquoted_text):
    return r'(?::(?P<api_name>{value_regex}))?'.format(value_regex=value_regex_part(forbidden_chars_in_unquoted_text))


def numeric_value_regex_part():
    return r'(?:-?\d+(?:\.\d+)?)'


def range_brackets_regex_part():
    return r'\(\s*(.+)\s*,\s*(.+)\s*,\s*(.+)\s*\)'


def range_regex_part():
    return r'\(\s*(?P<from>{number})\s*,\s*(?P<to>{number})\s*,\s*(?P<step>{number})\s*\)'.format(
        number=numeric_value_regex_part())


def list_brackets_regex_part(with_api_part=True):
    return r'(?P<value>\[(?:\s*(?:{value_regex})\s*(?:\s*,\s*(?:{value_regex})\s*)*)?\]){api_name_regex}$'.format( # pylint: disable=C0301
        value_regex=value_regex_part(FORBIDDEN_CHARS_IN_GRID_SEARCH_ARRAY),
        api_name_regex=optional_api_name_regex_part(DEFAULT_FORBIDDEN_CHARS) if with_api_part else r''
    )


SPACES_REGEX = re.compile(r'\s')
DASHED_FLAG_REGEX = re.compile(r'--?([^-\s\d]\S*)\s+$')

REFERENCE_PARAMETER_REGEX = re.compile(
    r'{api_name_regex}$'.format(
        api_name_regex=optional_api_name_regex_part(DEFAULT_FORBIDDEN_CHARS)
    )
)

SIMPLE_PARAMETER_REGEX = re.compile(
    r'(?P<value>{value_regex}){api_name_regex}$'.format(
        value_regex=value_regex_part(DEFAULT_FORBIDDEN_CHARS),
        api_name_regex=optional_api_name_regex_part(DEFAULT_FORBIDDEN_CHARS)
    )
)

GRID_SEARCH_ARRAY_FIND_BRACES_REGEX = re.compile(
    list_brackets_regex_part()
)

GRID_SEARCH_ARRAY_FIND_TOKENS_REGEX = re.compile(
    r'\s*,?\s*({value_regex})'.format(
        value_regex=value_regex_part(FORBIDDEN_CHARS_IN_GRID_SEARCH_ARRAY)
    )
)

GRID_SEARCH_RANGE_REGEX = re.compile(
    r'(?P<value>{range}){api_name}$'.format(
        range=range_regex_part(),
        api_name=optional_api_name_regex_part(DEFAULT_FORBIDDEN_CHARS)
    )
)
