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

import re


def cut_if_too_long(text, max_len=80, cut_marker="(...)", tail=False):
    if len(text) <= max_len:
        return text
    else:
        if tail:
            return cut_marker + text[-(max_len - len(cut_marker)):]
        else:
            return text[:max_len - len(cut_marker)] + cut_marker


def is_camel_case(phrase):
    if phrase:
        search = re.search(r"\s", phrase)
        return (not search) and (phrase[0].lower() == phrase[0])
    else:
        return True


def to_camel_case(phrase):
    if is_camel_case(phrase):
        return phrase
    else:
        pascal_case = ''.join(x for x in capitalize_words(phrase) if not x.isspace())
        camel_case = pascal_case[0].lower() + pascal_case[1:]
        return camel_case


def capitalize_words(s):
    result = re.sub(r'\w+', lambda m: m.group(0).capitalize(), s)
    return result


def is_float(value):
    try:
        _ = float(value)
    except ValueError:
        return False
    else:
        return True
