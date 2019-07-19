#
# Copyright (c) 2018, deepsense.io
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
import os
import shutil


class Directory(object):
    def __init__(self, path):
        self.__absolute_path = path

    @property
    def absolute_path(self):
        return self.__absolute_path

    def mkdir(self, name):
        subdir = self.subdir(name)
        if not os.path.exists(subdir.absolute_path):
            os.mkdir(subdir.absolute_path)
        return subdir

    def copy_to_subdir(self, src, dst_subdir_name):
        subdir = self.subdir(dst_subdir_name)
        shutil.copytree(src=src, dst=subdir.absolute_path)
        return subdir

    def subdir(self, name):
        return Directory(os.path.join(self.absolute_path, name))
