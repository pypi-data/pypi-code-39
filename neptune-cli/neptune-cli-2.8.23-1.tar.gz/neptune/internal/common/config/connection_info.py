#
# Copyright (c) 2018, deepsense.io
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
from neptune.internal.common.api.address import http_url_from_address, Address, rest_url_from_address, \
    ws_url_from_address
from neptune.internal.common.config.host_parser import HostParser, PortParser, SecureParser


class ConnectionInfo(object):
    HOST_PARSER = HostParser()
    PORT_PARSER = PortParser()
    SECURE_PARSER = SecureParser()

    def __init__(self,
                 username=None,
                 address=None,
                 frontend_address=None):
        self.username = username
        self.address = Address(
            host=self.HOST_PARSER.parse(address),
            port=self.PORT_PARSER.parse(address)
        )
        self.frontend_address = Address(
            host=self.HOST_PARSER.parse(frontend_address),
            port=self.PORT_PARSER.parse(frontend_address)
        )
        self.secure = self.SECURE_PARSER.parse(address) == 'https'

    @property
    def http_url(self):
        return http_url_from_address(self.address, self.secure)

    @property
    def rest_url(self):
        return rest_url_from_address(self.address, self.secure)

    @property
    def ws_url(self):
        return ws_url_from_address(self.address, self.secure)

    @property
    def frontend_http_url(self):
        return http_url_from_address(self.frontend_address, self.secure)

    @property
    def auth_code_http_url(self):
        return self.frontend_http_url + '/getting-started?showToken=true'
