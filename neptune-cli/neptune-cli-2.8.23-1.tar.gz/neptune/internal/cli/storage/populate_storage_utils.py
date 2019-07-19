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
from __future__ import print_function

import fnmatch
import os
import sys

import humanize
from kitchen.i18n import to_bytes, to_unicode
from pathlib2 import Path
from tqdm import tqdm

from neptune.internal.cli.commands.parsers.utils.validators import ArgumentsValidationException
from neptune.internal.common.utils.paths import join_paths
from neptune.internal.common.utils.system import IS_WINDOWS

to_unicode = to_unicode
to_bytestring = to_bytes

# pylint:disable=no-member

class CopySizeCounter(object):

    def __init__(self, description):
        self.size = 0
        self.description = description

    @staticmethod
    def _print(msg, size):
        print(u"\r{msg}: {size}".format(msg=msg,
                                        size=humanize.naturalsize(size, format=u"%.2f").ljust(10)),
              end=u'', file=sys.stderr)
        sys.stderr.flush()

    def add(self, src_path, dst_path):
        # pylint: disable=unused-argument
        self.size += os.path.getsize(src_path)
        self._print(u"Calculating {} size".format(self.description), self.size)

    def finalize(self):
        self._print(u"\rCalculated {} size".format(self.description), self.size)
        print(u"")


class CopyProgressBar(object):

    def __init__(self, total_size, desc=u"Creating experiment snapshot"):
        self.progress_bar = tqdm(desc=desc,
                                 total=total_size,
                                 unit=u'B',
                                 unit_scale=True,
                                 file=sys.stderr,
                                 ascii=IS_WINDOWS)

    def set_description(self, desc=None):
        self.progress_bar.set_description(desc)

    def update(self, block_size):
        self.progress_bar.update(block_size)

    def finalize(self):
        self.progress_bar.close()


def _create_filter_list(exclude):
    filter_list = []
    if exclude:
        for pattern in exclude:
            if os.path.isabs(pattern):
                raise ArgumentsValidationException(
                    u"Invalid exclude pattern: exclude patterns must be relative")
            filter_list.append(pattern)
            filter_list.append("*"+os.sep+pattern)
            filter_list.append(pattern+os.sep+"*")
            filter_list.append("*"+os.sep+pattern+os.sep+"*")
    return filter_list


def collect_files(p=None, exclude=None, description=u"experiment snapshot"):
    if p is None:
        p = "."

    # Remove trailing '/' chars.
    if exclude is not None:
        exclude = [e.rstrip(os.sep) for e in exclude]

    counter = CopySizeCounter(description)

    filter_list = _create_filter_list(exclude)

    files_list = []
    empty_dir_list = []

    path = Path(p).resolve()

    if path.is_dir():
        # get list of all files and directories under target path
        found_files = sorted([(
            found_file.absolute(),
            found_file.relative_to(path),
            join_paths(p, str(found_file.relative_to(path)))
        ) for found_file in path.glob('**' + os.sep + '*')])

        if not found_files:
            empty_dir_list.append((str(path.resolve()), path.resolve().name))

        for file_path in found_files:
            # skip files that match any of the exclude patterns
            if not any(fnmatch.fnmatch(str(file_path[1]), pattern) for pattern in filter_list):
                if file_path[0].is_dir():
                    # add all directories - non-empty ones are removed later
                    empty_dir_list.append((str(file_path[0]), str(file_path[2])))
                else:
                    files_list.append((str(file_path[0]), str(file_path[2])))
                    counter.add(str(file_path[0]), None)
    else:
        files_list.append((str(path.resolve()), path.resolve().name))
        counter.add(str(path.resolve()), None)

    counter.finalize()

    return files_list, counter.size, empty_dir_list
