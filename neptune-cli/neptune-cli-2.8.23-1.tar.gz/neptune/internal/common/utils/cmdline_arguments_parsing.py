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


def find_outside_of_quotes(pattern, text, must_be_preceded_by_whitespace=False):
    pattern_start_indices = []
    inside_double_quotes = False
    inside_single_quotes = False

    def inside_quotes():
        return inside_double_quotes or inside_single_quotes

    def unescaped_single_quote(prev_char, char):
        return char == u"'" and prev_char != u'\\'

    def unescaped_double_quote(prev_char, char):
        return char == u'"' and prev_char != u'\\'

    for index, (prev_char, char) in enumerate(zip([None] + list(text)[:-1], text)):
        if inside_double_quotes and unescaped_double_quote(prev_char, char):
            inside_double_quotes = False
        elif inside_single_quotes and unescaped_single_quote(prev_char, char):
            inside_single_quotes = False
        elif not inside_quotes() and unescaped_double_quote(prev_char, char):
            inside_double_quotes = True
        elif not inside_quotes() and unescaped_single_quote(prev_char, char):
            inside_single_quotes = True
        elif text[index:].startswith(pattern) and not inside_quotes() and \
                (not must_be_preceded_by_whitespace or index == 0 or prev_char.isspace()):
            pattern_start_indices.append(index)
    return pattern_start_indices
