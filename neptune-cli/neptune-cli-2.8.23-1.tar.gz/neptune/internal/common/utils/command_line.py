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
from future.builtins import range

import re

from neptune.internal.common.utils.system import IS_WINDOWS


def split_arguments(s, windows=IS_WINDOWS):
    # from http://stackoverflow.com/a/35900070
    r"""Multi-platform variant of shlex.split() for command-line splitting.
    For use with subprocess, for argv injection etc. Using fast REGEX.

    It solves problem with \ character that is always considered an escape character on unix, but
    on windows it's conditional.
    For example: c:\normal\windows\path on unix is expected to be c:normalwindowspath
    but on windows it stays the same. Still we want to be able to escape special characters like
    quotation mark and be able to pass json as one argument with the same command on both platforms.

    windows:
        True = Windows/CMD
        False = POSIX
    """
    if windows:
        RE_CMD_LEX = r'''"((?:""|\\["\\]|[^"])*)"?()|(\\\\(?=\\*")|\\")'
                     r'|(&&?|\|\|?|\d?>|[<])|([^\s"&|<>]+)|(\s+)|(.)'''
    else:
        RE_CMD_LEX = r'''"((?:\\["\\]|[^"])*)"|'([^']*)'|(\\.)|'
                     r'(&&?|\|\|?|\d?\>|[<])|([^\s'"\\&|<>]+)|(\s+)|(.)'''

    args = []
    accu = None  # collects pieces of one arg
    for qs, qss, esc, pipe, word, white, fail in re.findall(RE_CMD_LEX, s):
        if word:
            pass  # most frequent
        elif esc:
            word = esc[1]
        elif white or pipe:
            if accu is not None:
                args.append(accu)
            if pipe:
                args.append(pipe)
            accu = None
            continue
        elif fail:
            raise ValueError("invalid or incomplete shell string")
        elif qs:
            word = qs.replace('\\"', '"').replace('\\\\', '\\')
            if windows:
                word = word.replace('""', '"')
        else:
            word = qss  # may be even empty; must be last

        accu = (accu or '') + word

    if accu is not None:
        args.append(accu)

    return args


def merge_arguments_using_double_quotes(args):
    return list2cmdline(args)


def list2cmdline(seq):
    """ Extended version of list2cmdline from subprocess.

    Additional conditions sufficient to wrap argument with double quotes are added:

    * argument contains parenthesis.

    """

    result = []
    needquote = False
    for arg in seq:
        bs_buf = []

        # Add a space to separate this argument from the others
        if result:
            result.append(' ')

        needquote = (" " in arg) or ("\t" in arg) or (not arg) or ("(" in arg) or (")" in arg)
        if needquote:
            result.append('"')

        for c in arg:
            if c == '\\':
                # Don't know if we need to double yet.
                bs_buf.append(c)
            elif c == '"':
                # Double backslashes.
                result.append('\\' * len(bs_buf) * 2)
                bs_buf = []
                result.append('\\"')
            else:
                # Normal char
                if bs_buf:
                    result.extend(bs_buf)
                    bs_buf = []
                result.append(c)

        # Add remaining backslashes, if any.
        if bs_buf:
            result.extend(bs_buf)

        if needquote:
            result.extend(bs_buf)
            result.append('"')

    return ''.join(result)


def with_removed_option(args, option_name, until='--'):
    filtered_args = []
    skipping_values = False

    for idx in range(0, len(args)):
        if args[idx] == until:
            filtered_args += args[idx:]
            break
        if skipping_values and args[idx].startswith('--'):
            skipping_values = False
        if not skipping_values:
            if '--' + option_name == args[idx]:
                skipping_values = True
            else:
                filtered_args += [args[idx]]
    return filtered_args
