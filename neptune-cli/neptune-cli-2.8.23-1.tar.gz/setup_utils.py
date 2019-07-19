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
import shutil


def migrate_tokens():
    home_dir = expanduser(u'~')
    old_tokens_dir = os.path.join(home_dir, u'.neptune_tokens')
    local_storage_dir = os.path.join(home_dir, u'.neptune')

    if os.path.isdir(old_tokens_dir) and not os.path.exists(local_storage_dir):
        os.makedirs(local_storage_dir)
        new_tokens_dir = os.path.join(local_storage_dir, u'tokens')
        shutil.move(old_tokens_dir, new_tokens_dir)


def migrate_to_profile():
    home_dir = expanduser(u'~')
    old_tokens_dir = os.path.join(home_dir, u'.neptune', u'tokens')
    default_storage_dir = os.path.join(home_dir, u'.neptune', u'profile', u'default')

    if os.path.isdir(old_tokens_dir) and not os.path.isdir(default_storage_dir):
        new_tokens_dir = os.path.join(default_storage_dir, u'tokens')
        os.makedirs(default_storage_dir)
        shutil.move(old_tokens_dir, new_tokens_dir)

        global_config_location = os.path.join(home_dir, u'.neptune.yaml')
        if os.path.isfile(global_config_location):
            new_config_location = os.path.join(default_storage_dir, u'.neptune.yaml')
            shutil.move(global_config_location, new_config_location)
