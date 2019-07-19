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
import logging
import os
from distutils.errors import DistutilsFileError  # pylint: disable=import-error,no-name-in-module
from distutils.file_util import copy_file as distutils_copy_file  # pylint: disable=import-error,no-name-in-module,line-too-long

from neptune.internal.common.utils.paths import (
    absolute_path,
    make_path,
    join_paths)

_logger = logging.getLogger(__name__)


def copy_tree(src, dst, exclude=None, preserve_mode=0, preserve_times=0,
              preserve_symlinks=0, update=0, verbose=1, dry_run=0,
              post_file_copy_callback=lambda src_name, dst_name: None):
    """This is a copy of distutils.dir_util.copy_tree extended with parameters:
    'exclude' and 'post_file_copy_callback' and support of names with Unicode characters.
    The exclude parameter allows to exclude directories from being copied.
    The post_file_copy_callback parameter allows to provide callback called after file copy.

    The changes between this function and the original one are marked in the source code.
    """

    exclude = [path_to_exclude for path_to_exclude in exclude] if exclude else []

    # Change: There was no exclude. By default the parameter should a value of an empty list.
    exclude = [absolute_path(e) for e in exclude] if exclude else []

    if not dry_run and not os.path.isdir(src):
        raise DistutilsFileError("cannot copy tree '{}': not a directory".format(src))
    try:
        names = os.listdir(src)
        # Change: remove excluded files from 'names' (a list with files to be copied).
        names = [n for n in names if join_paths(src, n) not in exclude]
    except os.error as error:
        (_, errstr) = error.args
        if dry_run:
            names = []
        else:
            raise DistutilsFileError("error listing files in '{}': {}".format(src, errstr))

    if not dry_run:
        make_path(dst, verbose=verbose)

    outputs = []

    for n in names:
        src_name = os.path.join(src, n)
        dst_name = os.path.join(dst, n)

        if n.startswith('.nfs'):
            # skip NFS rename files
            continue

        if preserve_symlinks and os.path.islink(src_name):
            # os.readline and os.symlink doesn't exist on Windows
            # but os.path.islink always returns false.

            # pylint:disable=no-member
            link_dest = os.readlink(src_name)
            if verbose >= 1:
                _logger.info("linking %s -> %s", dst_name, link_dest)
            if not dry_run:
                os.symlink(link_dest, dst_name)
            outputs.append(dst_name)

        elif os.path.isdir(src_name):
            outputs.extend(
                # Change: supply exclude and post_file_copy_callback to recursive call
                copy_tree(src_name, dst_name, exclude, preserve_mode,
                          preserve_times, preserve_symlinks, update,
                          verbose=verbose, dry_run=dry_run,
                          post_file_copy_callback=post_file_copy_callback))
        else:
            distutils_copy_file(src_name, dst_name, preserve_mode,
                                preserve_times, update, verbose=verbose,
                                dry_run=dry_run)
            # Change: call provided post_file_copy_callback
            post_file_copy_callback(src_name, dst_name)
            outputs.append(dst_name)

    return outputs
