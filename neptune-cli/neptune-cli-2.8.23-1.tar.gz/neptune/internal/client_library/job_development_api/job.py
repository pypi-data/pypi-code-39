# -*- coding: utf-8 -*-
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

from __future__ import print_function

import sys

from future.builtins import object
from future.utils import itervalues, listvalues

from neptune.generated.swagger_client import models
from neptune.internal.client_library import (
    DuplicatedActionNamesException,
    InvalidActionNameException,
    DuplicatedChannelNamesException
)
from neptune.internal.client_library.job_development_api.action import Action
from neptune.internal.client_library.job_development_api.channel import Channel, AutoIncrementType
from neptune.internal.client_library.job_development_api.channel_params import ChannelParams
from neptune.internal.client_library.job_development_api.channel_type import ChannelType
from neptune.internal.client_library.job_development_api.image import Image
from neptune.internal.common.api import api_model_factories
from neptune.internal.common.models.parameters_validation import (
    function_arity,
    of_type_validator,
    one_of_validator,
    one_of_type_validator,
    float_conv,
    text_conv,
    validate,
    validate_coordinates)
from neptune.internal.common.utils.neptune_warnings import JobDeprecationWarning, neptune_warn


class Job(object):

    @staticmethod
    def _deprecation_warning(f_name):
        return "'{0}' method in 'job' object is deprecated and will be removed in future releases. ".format(f_name) + \
               "Please call this method directly from the context object (see " + \
               "http://docs.neptune.ml/advanced-topics/context)."

    def __init__(self, api_service, experiment_id, state, actions, properties, tags, metric, integration,
                 services, channels):
        self._api_service = api_service
        self._id = experiment_id
        self._state = state
        self._properties = properties
        self._tags = tags
        self._services = services
        self._integration = integration
        self.metric = metric
        self._channels = {}
        self._actions = actions
        for swagger_channel in channels:
            self._register_channel_internally(swagger_channel, AutoIncrementType.Int)
        for action in itervalues(actions):
            self._register_action_internally(action.name, None)

    def integrate_with_tensorflow(self):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        return self._integration.integrate_with_tensorflow(self)

    def integrate_with_keras(self):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)
        return self._integration.integrate_with_keras(self)

    @validate(
        name=text_conv,
        channel_type=one_of_validator([ChannelType.NUMERIC, ChannelType.TEXT, ChannelType.IMAGE])
    )
    def create_channel(self, name, channel_type, auto_increment_type=AutoIncrementType.Int):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        existing_channel = self._channels.get(name, None)
        if existing_channel:
            if existing_channel.type == channel_type and existing_channel.auto_increment_type == auto_increment_type:
                return existing_channel
            else:
                raise DuplicatedChannelNamesException(existing_channel)

        new_channel_params = ChannelParams(name, channel_type)

        swagger_new_channel = self._api_service.create_channel(self._id, new_channel_params)

        return self._register_channel_internally(swagger_new_channel, auto_increment_type)

    def _register_channel_internally(self, swagger_new_channel, auto_increment_type):
        new_channel = Channel(
            channel_values_service=self._services.channel_values_service,
            _id=swagger_new_channel.id,
            name=swagger_new_channel.name,
            channel_type=swagger_new_channel.channel_type,
            auto_increment_type=auto_increment_type)

        self._channels[new_channel.name] = new_channel

        return new_channel

    @validate_coordinates
    def channel_send(self, name, x=None, y=None):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        return self._channel_send(name, x, y)

    @validate(
        name=text_conv,
        y=one_of_type_validator([of_type_validator(Image), float_conv, text_conv]))
    def _channel_send(self, name, x=None, y=None):
        channel = self._channels.get(name, None)
        if not channel:
            chl = self.create_channel(name=name, channel_type=ChannelType.get_channel_type(y))
            chl.send(x=x, y=y)
            return chl
        else:
            channel.send(x=x, y=y)
            return channel

    def channel_reset(self, name):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        return self._channel_reset(name)

    def _reset_all_channels(self):
        for channel in itervalues(self._channels):
            channel.reset()

    def _delete_channel(self, name):
        return self._channel_delete(name)

    def _delete_all_channels(self):
        for channel in itervalues(self._channels):
            channel.delete()

    @validate(name=text_conv)
    def _channel_reset(self, name):
        channel = self._channels.get(name, None)
        if channel:
            channel.reset()
        else:
            print("neptune: warning: There is no channel named '{}'".format(str(name)))

    @validate(name=text_conv)
    def _channel_delete(self, name):
        channel = self._channels.get(name, None)
        if channel:
            channel.delete()
        else:
            print("neptune: warning: There is no channel named '{}'".format(str(name)))

    @validate(name=text_conv, handler=function_arity(1))
    def register_action(self, name, handler):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        if name is None or len(name.strip()) == 0:
            raise InvalidActionNameException(name)
        found_action = [found_action for found_action in itervalues(self._actions) if found_action.name == name]
        if found_action and found_action[0].handler:
            raise DuplicatedActionNamesException(name)

        action = self._register_action_internally(name, handler)

        if not found_action:
            experiment_params = models.EditExperimentParams()
            experiment_params.actions = api_model_factories.ActionApiModelFactory.create_actions(
                listvalues(self._actions))
            self._api_service.update_experiment(experiment_id=self._id, edit_experiment_params=experiment_params)

        return action

    def _register_action_internally(self, name, handler):
        action = Action(name, handler)

        self._actions[action.id] = action

        return action

    @property
    def id(self):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        return self._id

    @property
    def state(self):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        return self._state

    @property
    def tags(self):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        return self._tags

    @tags.setter
    def tags(self, new_tags):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        self._tags.set_tags(new_tags)

    @property
    def properties(self):
        neptune_warn(self._deprecation_warning(sys._getframe().f_code.co_name), # pylint: disable=W0212
                     JobDeprecationWarning)

        return self._properties
