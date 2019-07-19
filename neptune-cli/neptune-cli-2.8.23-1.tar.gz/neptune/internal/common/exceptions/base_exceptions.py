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


class NeptuneException(Exception):
    pass


class NeptuneIOException(NeptuneException):
    def __init__(self, io_error):
        message = "[Errno {}] {}: '{}'.".format(
            io_error.errno, io_error.strerror, io_error.filename)
        super(NeptuneIOException, self).__init__(message)
        self.message = message


class NeptuneInternalException(Exception):
    def __init__(self, msg):
        super(NeptuneInternalException, self).__init__(msg)
        self.message = msg


class NeptuneThreadInterruptedException(NeptuneInternalException):
    def __init__(self):
        super(NeptuneThreadInterruptedException, self).__init__('Thread interrupted')
