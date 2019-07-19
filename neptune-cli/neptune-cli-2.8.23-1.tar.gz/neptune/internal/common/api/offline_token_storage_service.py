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
import io
import json
import os
import shutil
import uuid

from neptune.internal.common.api.tokens import CompositeToken

TOKEN_FILENAME = 'token'


class OfflineTokenStorageService(object):

    def __init__(self, token_dirpath):

        self.token_dirpath = token_dirpath
        self.current_token_filepath = os.path.join(token_dirpath, TOKEN_FILENAME)

    def save(self, token):
        filepath = os.path.join(self.token_dirpath, str(uuid.uuid4()))

        with io.open(filepath, "w", encoding='utf-8') as token_file:
            token_file.write(json.dumps(token.raw, ensure_ascii=False))

        os.chmod(filepath, 0o600)
        shutil.copy2(filepath, self.current_token_filepath)

    def load(self):
        try:
            with io.open(self.current_token_filepath, "r", encoding='UTF-8') as token_file:
                return CompositeToken.from_json(json.load(token_file))
        except IOError:
            return None

    def clear(self):
        shutil.rmtree(self.token_dirpath)

    def contains_token(self):
        return os.path.isdir(self.token_dirpath) and len(os.listdir(self.token_dirpath)) > 0

    @classmethod
    def create(cls, token_dirpath, token=None):

        if not os.path.exists(token_dirpath):
            os.makedirs(token_dirpath)
            os.chmod(token_dirpath, 0o700)

        storage = cls(token_dirpath)

        if token:
            storage.save(token)

        return storage
