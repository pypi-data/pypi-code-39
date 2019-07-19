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
from __future__ import print_function
from future.builtins import object


class PaymentsUtils(object):
    def __init__(self,
                 config):
        """
        :type config:
        """
        self.config = config

    def print_insufficient_funds(self):
        frontend_url = u"{frontend_url}/?noFunds".format(
            frontend_url=self.config.frontend_http_url
        )

        print(
            u">\n" +
            u"> Insufficient funds, follow:\n" +
            u"> {frontend_url}\n>\n".format(frontend_url=frontend_url)
        )
