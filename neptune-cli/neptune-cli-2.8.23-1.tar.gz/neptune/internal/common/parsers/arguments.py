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

from neptune.internal.common.utils.str import to_bytestring


class Arguments(object):
    def __init__(self, raw_args, known_args):
        self.raw_args = raw_args
        self.known_args = known_args

    def __unicode__(self):
        u"Arguments({}, {})".format(self.raw_args, self.known_args)

    def __str__(self):
        return to_bytestring(self.__unicode__())

    def __eq__(self, other):
        return self.raw_args == other.raw_args and\
            self.known_args == other.known_args

    def add_known_args(self, name, value):
        setattr(self.known_args, name, value)
