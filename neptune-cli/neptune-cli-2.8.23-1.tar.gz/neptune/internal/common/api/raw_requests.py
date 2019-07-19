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
from future.utils import raise_from
import requests

from neptune.internal.cli.commands.experiment.ls.exceptions import ConnError, StatusCodeError


def raw_http_get(session, url, params, headers, timeout):
    response = None

    try:
        response = session.get(url, params=params, headers=headers, timeout=timeout)
    except (requests.ConnectionError, requests.Timeout) as error:
        raise_from(ConnError(), error)

    if response.status_code != 200:
        raise StatusCodeError(response.status_code)

    return response
