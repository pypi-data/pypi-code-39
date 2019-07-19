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

from future.builtins import object, str

from neptune.generated.swagger_client.path_constants import REST_PATH, WS_PATH


class Address(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __str__(self):
        _port_part = ':' + str(self.port) if self.port else ''
        return self.host + _port_part

    def to_url(self):
        return str(self)


def http_url_from_address(address, secure):
    protocol = "https://" if secure else "http://"
    return protocol + address.to_url()


def rest_url_from_address(address, secure):
    return http_url_from_address(address, secure) + REST_PATH


def ws_url_from_address(address, secure):
    protocol = "wss://" if secure else "ws://"
    return protocol + address.to_url() + WS_PATH
