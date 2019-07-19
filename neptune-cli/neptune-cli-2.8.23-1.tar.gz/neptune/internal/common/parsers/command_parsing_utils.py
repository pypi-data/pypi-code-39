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


def compose_string_command(raw_args):
    return ' '.join([maybe_quote_argument(arg) for arg in raw_args])


def maybe_quote_argument(arg):
    if arg.replace(u'.', '').replace(u'-', '').replace(u'_', '').isalnum():
        return arg
    else:
        return u'"' + arg.replace("\\", "\\\\").replace(u'"', u'\\"') + u'"'

def maybe_quote_argument_by_neptune_language(arg):
    if arg.replace(u'.', '').replace(u'-', '').replace(u'_', '').isalnum():
        return arg
    else:
        return u'"' + arg.replace(u'"', u'""') + u'"'

def compose_exec_args_template(args):
    if args == [u'']:
        return u'""'
    return ' '.join([
        arg.replace("\\", "\\\\").replace(u" ", u"\\ ").replace(u"'", u"\\'").replace(u'"', u'\\"') for arg in args
    ])


def create_args_from_template(exec_args_template):
    if len(exec_args_template) == 0:
        return []
    tmp_str = ""
    found_slash = False
    found_single_quote = False
    found_double_quote = False
    result = []
    for c in exec_args_template:
        if found_slash:
            found_slash = False
            tmp_str += c
        elif c == u'\\':
            found_slash = True
        elif (found_single_quote and c == "'") or (found_double_quote and c == '"'):
            found_single_quote = False
            found_double_quote = False
        elif not found_single_quote and c == "'" and not found_double_quote:
            found_single_quote = True
        elif not found_double_quote and c == '"' and not found_single_quote:
            found_double_quote = True
        elif c == u' ' and not found_single_quote and not found_double_quote:
            result.append(tmp_str)
            tmp_str = u''
        else:
            tmp_str += c
    result.append(tmp_str)
    return result
