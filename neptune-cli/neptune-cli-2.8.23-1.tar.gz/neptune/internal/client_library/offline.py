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
from __future__ import print_function

from future.builtins import object

import logging
import sys
import uuid

from neptune.generated.swagger_client import Channel
from neptune.internal.client_library.job_development_api.channel_type import ChannelType
from neptune.internal.client_library.job_development_api.context_params import ContextParams
from neptune.internal.common.utils import is_float

logger = logging.getLogger('job')


class OfflineUtilitiesService(object):

    def get_config_info(self):
        return {}


class OfflineTags(list):

    def set_tags(self, tags):
        del self[:]
        self.extend(tags)

    @classmethod
    def create_from(cls, existing_tags=None):

        tags = cls()

        if existing_tags:
            tags.extend(existing_tags)

        return tags


class OfflineContextParams(ContextParams):

    nonexistent_parameter_message = (
        u"neptune: Trying to access the '{}' parameter which is not defined.\n"
        u"         In order to run a Neptune job offline, you need to provide all parameters\n"
        u"         via offline_parameters argument of neptune.Context function.")

    def __getattribute__(self, key):

        try:
            return super(OfflineContextParams, self).__getattribute__(key)
        except AttributeError:
            print(self.nonexistent_parameter_message.format(key), file=sys.stderr)
            raise

    @classmethod
    def create_without_commandline_arguments_from(cls, context_params):
        params = cls()

        for key in context_params:
            params.__setattr__(key, context_params[key], immutable=False)

        return params


class OfflineIntegration(object):

    def __init__(self):
        self._integrator = None

    def integrate_with_tensorflow(self, *_):
        logger.debug('Offline Mode: Omitting integration with tensorflow.')

    def integrate_with_keras(self, *_):
        logger.debug('Offline Mode: Omitting integration with keras.')


class OfflineServices(object):

    def __init__(self, channel_values_service):
        self.channel_values_service = channel_values_service


class OfflineApiService(object):

    message = 'OfflineMode: Omitting Neptune API Service call.'

    def _log(self, *args, **kwargs):  # pylint:disable=unused-argument
        logger.debug(self.message)

    class OfflineObjectWithId(object):
        def __init__(self, _id):
            self.id = _id

    def __getattribute__(self, key):

        if key.startswith('update_'):
            return self._log
        elif key == 'create_channel':
            return lambda *args, **kwargs: self._create_channel(args[0], args[1])
        elif key.startswith('create_'):
            return lambda *args, **kwargs: self.OfflineObjectWithId(uuid.uuid4())
        else:
            return super(OfflineApiService, self).__getattribute__(key)

    def _create_channel(self, _id, channel_params):
        return Channel(
            id=_id,
            name=channel_params.name,
            channel_type=channel_params.channel_type
        )


class OfflineChannelValuesService(object):

    numeric_log_template = "%10s: (x: %16s, y: %s)."
    text_log_template = "%10s: (x: %16s, y: %s)."
    image_log_template = "%10s: (x: %16s, y: (name: %s)."

    def send(self, channel, x, y):

        if channel.type == ChannelType.NUMERIC:
            logger.info(self.numeric_log_template, channel.name, x, y)
        elif channel.type == ChannelType.TEXT:
            logger.info(self.text_log_template, channel.name, x, y)
        elif channel.type == ChannelType.IMAGE:
            logger.info(self.image_log_template, channel.name, x, y.name)

    def reset_channel(self, channel):
        pass

    def delete_channel(self, channel):
        pass


PARAMETER_TRANSFORMATION_RULES = [(lambda x: x.lower() in ('true', 'yes'), lambda _: True),
                                  (lambda x: x.lower() in ('false', 'no'), lambda _: False),
                                  (lambda x: x.isdigit(), int),
                                  (is_float, float)]
