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
import uuid

from future.builtins import object

from neptune.internal.common.utils.str import to_unicode


class TypeMapper(object):

    @staticmethod
    def to_bool(value):

        true_values = ["true", "t", "yes", "y", "1"]
        false_values = ["false", "f", "no", "n", "0"]
        if isinstance(value, bool):
            return value
        elif value.lower() in true_values:
            return True
        elif value.lower() in false_values:
            return False
        else:
            raise ValueError(
                u"Cannot convert: {} to bool. Supported values are: {}."
                .format(value, "[" + ", ".join(true_values + false_values) + "]"))

    @staticmethod
    def to_float(value):
        return float(value)

    @staticmethod
    def to_int(value):
        return int(value)


class TypeValidators(object):
    @staticmethod
    def uuid4_type(value):
        uuid.UUID(value, version=4)
        return to_unicode(value)
