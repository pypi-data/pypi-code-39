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
from future.builtins import str

import os
from distutils.dir_util import mkpath  # pylint: disable=import-error,no-name-in-module
from pathlib2 import Path

SRC_PATH = 'src'


def normalize_path(path):

    if path:
        split_drive, split_path = os.path.splitdrive(path)
        upper_drive = split_drive.upper()
        return os.path.normpath(os.path.join(upper_drive, split_path))
    else:
        return path


def resolve(p):
    return str(Path(p).resolve())


def getcwd():
    return resolve(os.getcwd())


def join_paths(path, *paths):
    joined_path = os.path.join(path, *paths)
    norm_joined_path = normalize_path(joined_path)
    return norm_joined_path


def absolute_path(path):
    abs_path = os.path.abspath(path)
    norm_abs_path = normalize_path(abs_path)
    return norm_abs_path


def make_path(dst, verbose=False):
    mkpath(dst, verbose=verbose)
    return dst
