# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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
# ==============================================================================
"""kv db"""
import atexit
import pickle
from datetime import datetime


class FastKV():
  def __init__(self, name=None, root=None, path=None):
    if path is not None:
      self.load(path)
    else:
      self._kv = {
          '_info': {
              'name': name,
              'root': root,
              'created_time': self._timestamp(),
              'modified_time': self._timestamp(),
          },
      }
    atexit.register(self._exit)

  def _exit(self):
    # do nothing
    # self.dump('final')
    pass

  def _timestamp(self):
    return datetime.strftime(datetime.now(), '%y%m%d%H%M%S')

  @property
  def kv(self) -> dict:
    return self._kv

  @property
  def info(self) -> dict:
    return self._kv['_info']

  def dump(self, step):
    export_path = '{}/{}.{}.kv.pkl'.format(self._kv['_info']['root'],
                                           self._kv['_info']['name'],
                                           step)
    with open(export_path, 'wb') as fw:
      pickle.dump(self._kv, fw)

  def load(self, path):
    with open(path, 'rb') as fp:
      self._kv = pickle.load(fp)

  def add(self, scope: str, value, step: int = -1):
    """scope: 'weight-layer0-max', step: 0, value: 3.14"""
    if scope not in self._kv:
      self._kv[scope] = {'step': [], 'value': []}
    self._kv[scope]['step'].append(step)
    self._kv[scope]['value'].append(value)
    self._kv['_info']['modified_time'] = self._timestamp()

  def get(self, scope: str):
    if scope in self._kv:
      return self._kv[scope]
    return None
