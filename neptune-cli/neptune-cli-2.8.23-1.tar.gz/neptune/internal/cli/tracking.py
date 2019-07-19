# -*- coding: utf-8 -*-
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
import logging
import platform
import time

import requests

from neptune import version
from neptune.internal.cli.commands.utils.git_utils import get_git_version

logger = logging.getLogger()


_TRACKING_URL = u'https://heapanalytics.com/api/track'
_TRACKING_APP_ID = u'3102000718'


class Timer(object):

    ''' Measure time elapsed in miliseconds. '''

    def __init__(self):
        self.start = self.end = self.elapsed = None

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.elapsed = (self.end - self.start) * 1000.0


def report_tracking_metrics(event, identity, timeout=1.0, **properties):

    properties.update(
        python_version=platform.python_version(),
        platform=platform.platform(),
        cli_version=version.__version__,
        git=(get_git_version() or u'not available')
        )

    body = {
        u'app_id': _TRACKING_APP_ID,
        u'identity': identity,
        u'event': event,
        u'properties': properties
    }

    try:
        requests.post(_TRACKING_URL, json=body, timeout=timeout)
        logger.debug('Track sent (%s)', body)
    except requests.exceptions.RequestException:
        logger.debug('Track request failed.')


def provide_default_user_identity_function(offline_token_storage_service):

    def get_user_identity_from_token():
        token = offline_token_storage_service.load()
        if token:
            return token.access_token.preferred_username or 'unknown'
        else:
            return 'unknown'

    return get_user_identity_from_token
