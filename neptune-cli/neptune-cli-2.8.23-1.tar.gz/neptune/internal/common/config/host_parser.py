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

from future import standard_library

standard_library.install_aliases()

# pylint: disable=wrong-import-position, import-error

from future.builtins import object

from urllib.parse import urlparse


class HostParser(object):

    def parse(self, host):
        if host is not None:
            host = host.strip()
            if host:
                parsed = urlparse(host)

                if parsed.scheme:
                    return self._value_from_parsed_url(parsed) or None
                else:
                    return self._value_from_parsed_url(parsed) or host

        return None

    @staticmethod
    def _value_from_parsed_url(url):
        if url.hostname:
            return url.hostname
        else:
            return None


class PortParser(object):

    def parse(self, address):
        if address is None or not address.strip():
            return None

        address = address.strip()
        parsed = urlparse(address)
        if parsed.port:
            return parsed.port
        else:
            return None


class SecureParser(object):

    def parse(self, address):
        if address is None or not address.strip():
            return None

        address = address.strip()
        parsed = urlparse(address)
        if parsed.scheme:
            return parsed.scheme
        else:
            return None
