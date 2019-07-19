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

from future.builtins import object

from neptune.generated.swagger_client import models


class PropertiesApiModelFactory(object):

    @classmethod
    def create_property(cls, key, value):
        api_property = models.KeyValueProperty()
        api_property.key = key
        api_property.value = value
        return api_property


class ActionApiModelFactory(object):

    @staticmethod
    def create_actions(actions):
        if actions is None:
            return None
        else:
            return [models.Action(action.id, action.name) for action in actions]
