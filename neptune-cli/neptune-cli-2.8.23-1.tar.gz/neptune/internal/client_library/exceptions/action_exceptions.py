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
from neptune.internal.common import NeptuneException
from neptune.internal.common.utils.str import to_bytestring


class DuplicatedActionNamesException(NeptuneException):
    def __init__(self, action_name):
        super(DuplicatedActionNamesException, self).__init__(
            u"Names of actions must be unique. Action '{}' already exists!" \
            .format(to_bytestring(action_name)))


class InvalidActionNameException(NeptuneException):
    def __init__(self, action_name):
        super(InvalidActionNameException, self).__init__(
            u"Name of an action has to be non-empty. Action name '{}' is invalid!" \
            .format(to_bytestring(action_name)))
