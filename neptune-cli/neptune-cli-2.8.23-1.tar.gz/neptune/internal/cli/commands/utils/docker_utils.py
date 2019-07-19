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


def resolve_docker_image(environment, api_service):

    if environment is None:
        return None

    envs = api_service.list_environments()

    env = next(iter([e for e in envs if e.name == environment]), None)

    if env is None:
        raise NeptuneException("Unknown environment '{}'.".format(environment))

    return "%s:%s" % (env.repository, env.tag)
