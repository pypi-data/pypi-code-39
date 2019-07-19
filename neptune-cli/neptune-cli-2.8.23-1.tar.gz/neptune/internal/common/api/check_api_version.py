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

import re

from neptune.internal.common.api.exceptions import (
    InvalidApiVersionException,
    NeptuneConnectionFailedException,
    NeptuneServerRequestFailedException,
    NeptuneServerResponseErrorException
)
from neptune.internal.common.api.utils import APIErrorCodes
from neptune.server import __version__ as server_api_version


class CheckApiVersion(object):

    def __init__(self, utilities_api_service, client_version, config):
        self._utilities_api_service = utilities_api_service
        self._client_version = client_version
        self._config = config
        self._check_connection()

    @property
    def client_version(self):
        return self._client_version

    def _check_connection(self):
        try:
            version_info = self._utilities_api_service.get_version()
            if version_info.version is None:
                raise NeptuneConnectionFailedException(self._config.http_url)
            self._check_version_compatibility(version_info.version)
        except NeptuneServerResponseErrorException as exc:
            # Old backends don't have an endpoint for obtaining version in root.
            # Bare backend returns 404 in such a case, but a proxy redirects to /login (302).
            if exc.status == APIErrorCodes.NOT_FOUND.value or\
                            exc.status == APIErrorCodes.MOVED.value:
                raise InvalidApiVersionException(
                    self.client_version,
                    backend_version='unknown')
            else:
                raise
        except NeptuneServerRequestFailedException:
            raise NeptuneConnectionFailedException(self._config.http_url)

    def _check_version_compatibility(self, backend_version):
        client_api_version = self.extract_api_version(self.client_version)
        backend_api_version = self.extract_api_version(backend_version)

        if backend_api_version is None:
            raise NeptuneConnectionFailedException(self._config.http_url)
        elif client_api_version != backend_api_version:
            raise InvalidApiVersionException(self.client_version, backend_version)

    @staticmethod
    def extract_api_version(version_string):
        match_result = re.match('\\d+\\.\\d+', version_string)
        if match_result:
            return match_result.group(0)
        else:
            return None

    @staticmethod
    def for_service(utilities_api_service, config):
        return CheckApiVersion(utilities_api_service, server_api_version, config)
