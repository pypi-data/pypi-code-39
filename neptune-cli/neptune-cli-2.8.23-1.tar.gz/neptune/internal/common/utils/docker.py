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


def convert_to_docker(path):
    def split_drive(p):
        if len(p) > 1 and p[1] == ':':
            return p[:1].lower(), p[2:]
        return None, None

    if path:
        path = path.replace('\\', '/')

    if not path or len(path.strip()) == 0:
        return path
    else:
        drive, dirs = split_drive(path)
        if drive:
            return "/" + drive + dirs
        elif path[0] == '/':
            return path
        raise CouldNotTransformPathToDockerPath(path)


class CouldNotTransformPathToDockerPath(NeptuneException):
    def __init__(self, path):
        self.path = path
        super(CouldNotTransformPathToDockerPath, self).__init__(
            u'Could not transform {} path to docker-internal path'.format(path))
