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
import logging
import threading
import re

from future.builtins import object
from requests_oauthlib import oauth2_session

from neptune.generated.analytics.swagger_client import CliUsageEvent, NeptuneCrashEvent, RestEvent
from neptune.internal.common.api.exceptions import NeptuneServerResponseErrorException
from neptune.version import __version__ as cli_version

oauth2_session.log.setLevel(logging.WARNING)


class AnalyticsApiService(object):
    def __init__(self, neptune_api_handler):
        self._logger = logging.getLogger(__name__)
        self._api_handler = neptune_api_handler

    def send_cli_usage_event_async(self, command_name, correct_usage, full_command, has_local_config):
        thread = threading.Thread(target=self.send_cli_usage_event,
                                  args=(command_name, correct_usage, full_command, has_local_config))
        thread.setDaemon(True)
        thread.start()

    def send_cli_usage_event(self, command_name, correct_usage, full_command, has_local_config, **kwargs):
        try:
            import locale
            import os
            import platform
            import sys
            locale.setlocale(locale.LC_ALL, "")

            event = RestEvent(cli_usage=CliUsageEvent(
                cli_version=cli_version,
                command_name=command_name,
                correct_usage=correct_usage,
                full_command=full_command,
                local_config=has_local_config,
                locale=".".join(locale.getlocale()),
                os="{}:{}:{}".format(os.name, platform.system(), platform.version()),
                python_version=sys.version
            ))
            return self._api_handler.feed_using_post(event_data=event, **kwargs)
        except Exception as e:
            self._logger.info("Unable to call analytics service: %s", e)

    def send_neptune_crash(self, exc):
        try:
            if isinstance(exc, NeptuneServerResponseErrorException):
                event = self._api_crash_event(exc)
            else:
                event = self._cli_crash_event(exc)
            return self._api_handler.feed_using_post(event_data=event)
        except Exception as e:
            self._logger.info("Unable to call analytics service: %s", e)

    def _api_crash_event(self, exc):
        experiments_url_match = re.compile(r'/experiments/([0-9a-f-]+)').search(exc.url)

        if experiments_url_match:
            experiment_id = experiments_url_match.group(1)
        else:
            experiment_id = None

        return RestEvent(neptune_crash=NeptuneCrashEvent(
            component='CLI',
            current_url=exc.url,
            experiment_id=experiment_id,
            logs=exc.body
        ))

    def _cli_crash_event(self, exc):
        return RestEvent(neptune_crash=NeptuneCrashEvent(
            component='CLI',
            current_url=None,
            experiment_id=None,
            logs=str(exc)
        ))
