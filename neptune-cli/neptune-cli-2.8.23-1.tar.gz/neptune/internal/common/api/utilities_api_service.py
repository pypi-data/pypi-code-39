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

import logging


class UtilitiesService(object):
    def __init__(self, neptune_api_handler, neptune_api_handler_without_auth):
        self._logger = logging.getLogger(__name__)
        self._api_handler = neptune_api_handler
        self._neptune_api_handler_without_auth = neptune_api_handler_without_auth

    def get_config_info(self):
        return self._api_handler.config_info_get()

    def get_version(self):
        return self._neptune_api_handler_without_auth.version_get()
