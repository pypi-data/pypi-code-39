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
from future.utils import PY3

from kitchen.i18n import to_bytes, to_unicode

to_unicode = to_unicode
to_bytestring = to_bytes


def map_recursively(mapping_fun):
    def apply_mapping(value):
        if isinstance(value, list):
            return [apply_mapping(el) for el in value]
        elif isinstance(value, dict):
            return {apply_mapping(key): apply_mapping(value)
                    for key, value in list(value.items())}
        elif isinstance(value, tuple):
            return tuple(apply_mapping(item) for item in value)
        else:
            return mapping_fun(value)
    return apply_mapping


def map_bytestring_to_unicode(value):
    def unicode_mapping(inner_value):

        if not PY3:
            if isinstance(inner_value, str):
                return to_unicode(inner_value)
            else:
                return inner_value

        else:

            if isinstance(inner_value, bytes):
                return inner_value.decode('utf-8')
            else:
                return inner_value

    return map_recursively(unicode_mapping)(value)


def map_unicode_to_bytestring(value):
    def byte_string_mapping(inner_value):

        # FIXME: This piece of code could be greatly simplified.

        if not PY3:

            if isinstance(inner_value, unicode):  # pylint:disable=undefined-variable
                return to_bytestring(inner_value)
            else:
                return inner_value

        else:

            if isinstance(inner_value, str):
                return inner_value.encode('utf-8')
            else:
                return inner_value
    return map_recursively(byte_string_mapping)(value)
