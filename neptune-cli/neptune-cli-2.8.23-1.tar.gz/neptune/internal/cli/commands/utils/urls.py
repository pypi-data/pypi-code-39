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

from future.builtins import object

from neptune.server import __api__ as api_prefix


class Urls(object):

    def __init__(self, rest_api_url):
        self.rest_api_url = rest_api_url

    @property
    def get_experiments_url(self):
        return self.rest_api_url + '/{api_prefix}/experiments'.format(api_prefix=api_prefix)
