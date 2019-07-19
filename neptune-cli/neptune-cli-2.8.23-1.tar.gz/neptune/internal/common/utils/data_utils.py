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

from future.utils import iteritems

import re


def decamelize_keys(dct):
    return update_dict_keys(dct, decamelize)


def update_dict_keys(obj, function):
    if isinstance(obj, dict):
        return {function(k): update_dict_keys(v, function) for k, v in iteritems(obj)}
    else:
        return obj


def decamelize(string, joiner='_'):
    """Convert a *CamelCase* `string` to a *lower_case* string.

    - The underscores can be changed to a custom `joiner` string.
    """

    def replace(match):
        prefix = (  # Don't prepend the joiner to the beginning of string
            '' if match.group(2) else joiner
        )
        caps = match.group(1).lower()
        follower = match.group(3)
        if not follower:
            return prefix + caps
        if len(caps) == 1:
            return prefix + caps + follower
        return prefix + caps[:-1] + joiner + caps[-1] + follower

    return re.sub('((^[A-Z]+)|[A-Z]+)([a-z])?', replace, string)
