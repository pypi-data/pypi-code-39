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
from os.path import expanduser

from neptune.internal.common.local_storage.directory import Directory
from neptune.internal.common.parsers.common_parameters_configurator import CommonParametersConfigurator


class LocalStorage(Directory):
    __EXPERIMENTS = u'experiments'
    __TOKENS = u'tokens'
    __SUBDIRS = [__EXPERIMENTS, __TOKENS]

    @classmethod
    def create(cls):

        return LocalStorage(path=os.path.join(expanduser(u'~'), CommonParametersConfigurator.NEPTUNE_DIRECTORY))

    @classmethod
    def profile(cls, profile='default'):
        profile_dir_path = os.path.join(os.path.expanduser(u'~'),
                                        CommonParametersConfigurator.NEPTUNE_DIRECTORY,
                                        CommonParametersConfigurator.PROFILE_DIRECTORY)

        profile_path_exists = os.path.exists(profile_dir_path)

        if not profile_path_exists:
            os.makedirs(profile_dir_path)

        user_profile_path = os.path.join(profile_dir_path, profile)
        storage = LocalStorage(path=user_profile_path)
        storage.create_directory_structure()
        return storage

    def create_directory_structure(self):
        if not os.path.exists(self.absolute_path):
            os.makedirs(self.absolute_path)
        for subdir in self.__SUBDIRS:
            self.mkdir(subdir)

    @property
    def experiments_directory(self):
        return Directory(os.path.join(self.absolute_path, self.__EXPERIMENTS))

    @property
    def tokens_directory(self):
        return Directory(os.path.join(self.absolute_path, self.__TOKENS))
