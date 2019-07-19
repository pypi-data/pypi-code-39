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
from neptune.internal.common import NeptuneException


class ReadOnlyException(NeptuneException):
    def __init__(self):
        cause = u"Parameters are immutable"
        super(ReadOnlyException, self).__init__(cause)


class CLIParameterParseException(NeptuneException):
    def __init__(self, parameter):
        cause = u'Parameter ' + parameter + u' wrong declaration'
        super(CLIParameterParseException, self).__init__(cause)


class RangeParameterParseException(NeptuneException):
    def __init__(self, parameter):
        cause = u"Wrong syntax for range parameter '" + parameter
        super(RangeParameterParseException, self).__init__(cause)
