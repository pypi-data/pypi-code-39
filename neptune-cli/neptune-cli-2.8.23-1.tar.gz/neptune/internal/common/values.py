# -*- coding: utf-8 -*-
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
from collections import namedtuple
import re

from future.builtins import str

from neptune.internal.common import NeptuneException


class UnknownUserError(NeptuneException):
    pass


class Tag(str):
    invalid = (
        "Invalid tag '{}'. Valid tags may contain only lowercase letters, digits, "
        "underscores and dashes."
    )

    @classmethod
    def create_from(cls, string):
        if re.match(r'^[\w-]+$', string, flags=re.U) is None:
            raise ValueError(cls.invalid.format(string))

        return cls(string)


class LogChannel(namedtuple('LogChannel', ['prefix', 'name'])):

    @classmethod
    def create(cls, prefix, name=None):
        if name is None:
            name = prefix.rsplit(u':', 1)[0]
        return cls(prefix, name)

    def __str__(self):
        return u':'.join([self.prefix, self.name])
