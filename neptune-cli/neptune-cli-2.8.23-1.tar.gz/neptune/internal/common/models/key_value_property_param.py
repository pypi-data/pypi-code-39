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

from neptune.generated.swagger_client import KeyValueProperty
from neptune.internal.common.utils.str import to_bytestring, to_unicode


class KeyValuePropertyParam(object):
    def __init__(self, key, value):
        self.key = to_unicode(key)
        self.value = to_unicode(value)

    def to_swagger_key_value_property(self):
        key_value_property = KeyValueProperty(self.key, self.value)
        return key_value_property

    def to_dict(self):
        return {self.key: self.value}

    def __repr__(self):
        return u"KeyValuePropertyParam({}, {})".format(self.key, self.value)

    def __unicode__(self):
        return u"{}:{}".format(self.key, self.value)

    def __str__(self):
        return to_bytestring(self.__unicode__())

    def __eq__(self, other):
        return isinstance(other, type(self)) and other.key == self.key and other.value == self.value
