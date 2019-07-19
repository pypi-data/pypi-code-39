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
from future.builtins import object

import os
import sys
import threading
import warnings

from PIL import Image

from neptune.generated.swagger_client import ExperimentState
from neptune.internal.cli.commands.utils.urls import Urls
from neptune.internal.cli.exceptions.params_exceptions import ReadOnlyException
from neptune.internal.cli.helpers import should_retry_api_calls
from neptune.internal.client_library.background_services.services import Services
from neptune.internal.client_library.job_development_api.channel import AutoIncrementType
from neptune.internal.client_library.job_development_api.context_params import ContextParams
from neptune.internal.client_library.job_development_api.job import Job
from neptune.internal.client_library.job_development_api.key_value_properties_service import \
    KeyValuePropertiesService
from neptune.internal.client_library.job_development_api.metric import Metric
from neptune.internal.client_library.job_development_api.tags_service import TagsService
from neptune.internal.client_library.offline import (OfflineApiService, OfflineChannelValuesService,
                                                     OfflineContextParams, OfflineIntegration, OfflineServices,
                                                     OfflineTags, OfflineUtilitiesService)
from neptune.internal.client_library.third_party_integration import ThirdPartyIntegration
from neptune.internal.common.api.job_api_service import JobApiService
from neptune.internal.common.api.keycloak_api_service import KeycloakApiConfig, KeycloakApiService
from neptune.internal.common.api.neptune_api.handler import create_base_neptune_api_handler, \
    create_base_neptune_api_handler_without_auth, create_neptune_api_handler
from neptune.internal.common.api.offline_token_storage_service import OfflineTokenStorageService
from neptune.internal.common.api.utilities_api_service import UtilitiesService
from neptune.internal.common.local_storage.local_storage import LocalStorage
from neptune.internal.common.utils.logging_utils import LogFileOpenError, OfflineNeptuneLogger, OnlineNeptuneLogger
from neptune.internal.common.utils.neptune_warnings import JobDeprecationWarning, JobPropertyDeprecationWarning, \
    ignore_deprecated, neptune_warn
from neptune.internal.common.websockets.reconnecting_websocket_factory import ReconnectingWebsocketFactory


class NeptuneContext(object):
    """ A Context represents a connection to Neptune Server and can be used to:

    .. warning:: For internal use only.

           Use :py:attr:`~neptune.Context` to create NeptuneContext instead.

    - access Experiment class to manage its lifecycle, access and modify objects connected to Experiment,
    - access ContextParams via params,
    - access and modify storage_url.

    """

    def __init__(self, experiment, params, utilities_service):
        self._experiment = experiment
        self._params = params
        self._utilities_service = utilities_service

    @property
    def job(self):
        """
        This method is deprecated and will be removed in the future release.

        Gets Experiment object from the Context.

        :return: An Experiment from the Context.
        """
        neptune_warn("'experiment' property in 'context' object is deprecated " +
                     "and will be removed in the future release. Please call experiment methods directly from " +
                     "the context object (see http://docs.neptune.ml/advanced-topics/context)"
                     , JobPropertyDeprecationWarning)

        return self._experiment

    @property
    @ignore_deprecated
    def experiment_id(self):
        """
        Gets id of the underlying Experiment.

        :return: The id of the Experiment.
        :rtype: uuid
        """
        return self._experiment.id

    @property
    @ignore_deprecated
    def state(self):
        """
        Gets state of underlying Experiment.

        :return: An experiment's state.
        :rtype: ExperimentState
        """
        return self._experiment.state

    @property
    @ignore_deprecated
    def tags(self):
        """
        Gets the set of user-defined tags for the experiment.
        Tags can be used for searching and marking experiments.

        Accessing tags::

            my_tag_exists = 'my-tag' in ctx.tags

        Modifying tags::

            ctx.tags.append('new-tag')
            ctx.tags.remove('new-tag')

        :return: A experiment's tags.
        :rtype: neptune.TagsService
        """
        return self._experiment.tags

    @tags.setter
    @ignore_deprecated
    def tags(self, new_tags):
        """
        Sets user-defined tags for the experiment.
        Tags can be used for searching and marking experiments.

        Modifying tags::

            ctx.tags = ['tag1', 'tag2', 'tag3']

        :param new_tags: list of new experiment's tags
        :return: Nothing
        """
        self._experiment.tags.set_tags(new_tags)

    @property
    @ignore_deprecated
    def properties(self):
        """
        Gets the set of user-defined properties of the Experiment.
        Properties are additional metadata of the experiment.
        A property is defined as a key-value pair of two strings.
        Experiment’s properties can be set from the configuration file and experiment’s code
        or by command line parameters.

        Accessing properties::

            print ctx.properties['my-property']

        Modifying properties::

            ctx.properties['property1'] = 'new-value'
            ctx.properties['property2'] = 'new-value'
            del(ctx.properties['property2'])

        :return: An experiment's properties.
        :rtype: collections.MutableMapping
        """
        return self._experiment.properties

    @property
    def params(self):
        """
        Gets the params of this Context.
        The set of user-defined variables passed to the experiment’s program.

        :return: The params of this Context.
        :rtype: neptune.ContextParams
        """
        return self._params

    @params.setter
    def params(self, _):
        raise ReadOnlyException()

    @property
    def metric(self):
        """
        Gets the metric used to compare the experiment with other experiments in the group.

        :return: The metric from the Context.
        :rtype: neptune.Metric
        """
        return self._experiment.metric

    def get_neptune_config_info(self):
        """
        Gets configuration information.

        :return: neptune config info.
        """
        return self._utilities_service.get_config_info()

    @ignore_deprecated
    def integrate_with_tensorflow(self):
        """
        Integrate Tensorflow with Neptune.

        """

        self._experiment.integrate_with_tensorflow()

    @ignore_deprecated
    def integrate_with_keras(self):
        """
        Integrate Keras with Neptune.

        """

        self._experiment.integrate_with_keras()

    @ignore_deprecated
    def create_channel(self, name, channel_type, auto_increment_type=AutoIncrementType.Int):
        """
        Creates a new channel with given name, type and optional extra parameters.

        Creating numeric and text channels::

            numeric_channel = ctx.create_channel(
                name='numeric_channel',
                channel_type=neptune.ChannelType.NUMERIC)

            text_channel = ctx.create_channel(
                name='text_channel',
                channel_type=neptune.ChannelType.TEXT)

            numeric_channel.send(x=1, y=2.5)
            numeric_channel.send(x=1.5, y=5)

            text_channel.send(x=2.5, y='text 1')
            text_channel.send(x=3, y='text 2')

        Creating an image channel::

            channel = ctx.create_channel(
                name='image_channel',
                channel_type=neptune.ChannelType.IMAGE)

            channel.send(
                x=1,
                y=neptune.Image(
                    name='#1 image name',
                    description='#1 image description',
                    data=Image.open("/home/ubuntu/image1.jpg")))


        :param name: A channel name. It must be unique in the scope of a specific experiment.
        :param channel_type: Type of the channel.
        :param auto_increment_type: Type of the x auto incrementing algorithm.
        :type name: unicode
        :type channel_type: neptune.ChannelType
        :type auto_increment_type: AutoIncrementType

        :return: Channel.
        :rtype: neptune.Channel
        """

        return self._experiment.create_channel(name, channel_type, auto_increment_type)

    @ignore_deprecated
    def channel_send(self, name, x=None, y=None):
        """
        Given values of X and Y and Name, sends a value to named Neptune channel,
        creating it if necessary.

        If the channel needs to be created, the type of the channel is determined
        based on type of Y value

        Calling
            ctx.channel_send(
                name='ch1',
                x=1.0,
                y=2.0)
        Is equivalent to:
            ch1 = ctx.create_channel(
                name='ch1',
                channel_type=neptune.ChannelType.NUMERIC)
            ch1.send(x=1.0, y=2.0)

        :param name: The name of the Neptune channel to use.
            If the channel does not exist yet, it is created with a type based on
            Y value type
        :param x: The value of channel value's X-coordinate.
            Values of the x parameter should be strictly increasing for consecutive calls.
            If this param is None, the last X-coordinate incremented by one will be used
        :param y: The value of channel value's Y-coordinate.
            Accepted types: float for :py:attr:`~neptune.series_type.NUMERIC`,
            str/unicode for :py:attr:`~neptune.series_type.TEXT`,
            neptune.Image for :py:attr:`~neptune.series_type.IMAGE`.

        :return: The channel used to send message to Neptune.
        :rtype: neptune.Channel
        """

        return self._experiment.channel_send(name, x, y)

    @ignore_deprecated
    def channel_reset(self, name):
        """
        Given a channel name, resets the channel.

        Calling
            ctx.channel_reset(name='ch1')
        Is equivalent to:
            ch1 = ctx.create_channel(
                name='ch1',
                channel_type=neptune.ChannelType.NUMERIC)
            ch1.reset()

        :param name: The name of the Neptune channel to use.
        """

        return self._experiment.channel_reset(name)

    def reset(self):
        """
        Delete all channels with their values
        """

        return self._experiment._delete_all_channels()  # pylint:disable=protected-access

    def delete_all_channels(self):
        """
        Delete all channels with their values
        """

        return self._experiment._delete_all_channels()  # pylint:disable=protected-access

    def reset_all_channels(self):
        """
        Remove all values from all channels
        """

        return self._experiment._reset_all_channels()  # pylint:disable=protected-access

    def delete_channel(self, name):
        """
        Delete channel with a given name and all its values

        :param name: The name of the Neptune channel to delete.
        """

        return self._experiment._delete_channel(name)  # pylint:disable=protected-access

    @ignore_deprecated
    def register_action(self, name, handler):
        """
        Registers a new action that calls handler with provided argument on invocation.

        Registering an action::

            session = ...

            def save_model(path):
                return str(session.save_model(path))

            ctx.register_action(name='save model', handler=save_model)

        :param name: Unique action name.
        :param handler: An one argument function that will be called on an action invocation.
                        Handler must take one unicode or str argument and return unicode or str
                        as the result.
        :type name: unicode
        :return: Action.
        :rtype: neptune.Action
        """

        return self._experiment.register_action(name, handler)


class ContextFactory(object):

    def __init__(self):
        if 'NEPTUNE_USER_PROFILE_PATH' in os.environ:
            self._local_storage = LocalStorage(os.environ["NEPTUNE_USER_PROFILE_PATH"])
        else:
            self._local_storage = LocalStorage.profile()

    offline_execution_message = u'neptune: Executing in Offline Mode.'

    logfile_open_error_message = (
        u"neptune: Cannot open logging file: {}.\n"
        u"         Sent channel values will not be logged during experiment execution.\n"
        u"         If you want to print sent channel values, you need to add following\n"
        u"         piece of code at the top of your experiment, after call to neptune.Context function:\n"
        u"\n"
        u"         import logging\n"
        u"         logging.getLogger('experiment').addHandler(logging.StreamHandler())")

    def create(self,
               cmd_line_args=None,
               tags=None,
               properties=None,
               offline_parameters=None,
               parent_thread=threading.current_thread(),
               with_retries=should_retry_api_calls()):

        warnings.simplefilter("once", JobDeprecationWarning)
        warnings.simplefilter("once", JobPropertyDeprecationWarning)

        if 'NEPTUNE_ONLINE_CONTEXT' in os.environ:
            return self._create_online_context(cmd_line_args, self._local_storage, parent_thread, with_retries)
        else:
            print(self.offline_execution_message, file=sys.stderr)
            return self._create_offline_context(context_params=offline_parameters, context_tags=tags,
                                                context_properties=properties)

    @staticmethod
    def _create_online_context(cmd_line_args, local_storage, parent_thread, with_retries):
        if cmd_line_args is None:
            cmd_line_args = get_cmdline_arguments()

        OnlineNeptuneLogger.configure_python_library_logging(cmd_line_args)

        keycloak_api_service = KeycloakApiService(KeycloakApiConfig())

        offline_token_storage_service = OfflineTokenStorageService.create(
            token_dirpath=local_storage.tokens_directory.absolute_path)

        neptune_rest_api_url = os.environ["NEPTUNE_REST_API_URL"]
        neptune_experiment_id = os.environ["NEPTUNE_JOB_ID"]


        preinit_PIL()

        api_service, utilities_service, tags_service, properties_service = create_online_services(
            Urls(neptune_rest_api_url),
            neptune_rest_api_url,
            neptune_experiment_id,
            offline_token_storage_service,
            with_retries=with_retries
        )
        experiment_api_model = api_service.get_experiment(neptune_experiment_id)
        group_api_model = api_service.get_group(experiment_api_model.group_id) if experiment_api_model.group_id \
                                                                                  is not None else None

        actions = {action.id: action for action in experiment_api_model.actions}
        channels = experiment_api_model.channels or []

        return NeptuneContext(
            experiment=Job(api_service=api_service,
                           experiment_id=neptune_experiment_id,
                           state=experiment_api_model.state,
                           channels=channels,
                           actions=actions,
                           tags=tags_service,
                           metric=create_metric(group_api_model),
                           properties=properties_service,
                           integration=ThirdPartyIntegration(),
                           services=Services(
                               neptune_experiment_id,
                               api_service,
                               utilities_service.get_config_info().max_form_content_size,
                               job_actions=actions,
                               parent_thread=parent_thread,
                               websocket_factory=ReconnectingWebsocketFactory(
                                   local_storage=local_storage,
                                   base_address=os.environ["NEPTUNE_WS_API_URL"],
                                   experiment_id=os.environ["NEPTUNE_JOB_ID"],
                                   offline_token_storage_service=offline_token_storage_service,
                                   keycloak_api_service=keycloak_api_service)).start()),
            params=ContextParams.create_from(experiment_api_model),
            utilities_service=utilities_service)

    def _create_offline_context(self, context_params, context_properties=None, context_tags=None):

        try:
            OfflineNeptuneLogger.configure_python_library_logging()
        except LogFileOpenError as error:
            print(self.logfile_open_error_message.format(error.path), file=sys.stderr)

        context_params = context_params or {}
        context_params = OfflineContextParams.create_without_commandline_arguments_from(context_params)

        return NeptuneContext(
            experiment=Job(api_service=OfflineApiService(),
                           experiment_id=None,
                           state=ExperimentState.running,
                           channels=[],
                           actions={},
                           tags=OfflineTags.create_from(context_tags),
                           metric=None,
                           properties=context_properties or {},
                           integration=OfflineIntegration(),
                           services=OfflineServices(OfflineChannelValuesService())),
            params=context_params,
            utilities_service=OfflineUtilitiesService())


def create_online_services(urls, rest_api_url, experiment_id, offline_token_storage_service, with_retries):
    """
    :rtype: (neptune.internal.common.api.job_api_service.JobApiService,
        UtilitiesService,
        TagsService,
        KeyValuePropertiesService)
    """

    base_api_handler_with_auth, requests_client_with_auth = \
        create_base_neptune_api_handler(rest_api_url, offline_token_storage_service)
    base_api_handler_without_auth = create_base_neptune_api_handler_without_auth(rest_api_url)

    neptune_api_handler_with_auth = create_neptune_api_handler(base_api_handler_with_auth)
    neptune_api_handler_without_auth = create_neptune_api_handler(base_api_handler_without_auth)

    utilities_service = UtilitiesService(
        neptune_api_handler_with_auth,
        neptune_api_handler_without_auth
    )
    api_service = JobApiService(
        urls,
        requests_client_with_auth,
        neptune_api_handler_with_auth,
        with_retries,
        utilities_service
    )

    tags_service = TagsService(experiment_id, neptune_api_handler_with_auth)
    properties_service = KeyValuePropertiesService(experiment_id, neptune_api_handler_with_auth)

    return api_service, utilities_service, tags_service, properties_service


def create_metric(group_api_model):
    if group_api_model is None:
        return None

    api_metric = group_api_model.metric

    if api_metric is not None:
        return Metric(channel_name=api_metric.channel_name, direction=api_metric.direction)
    else:
        return None


def get_cmdline_arguments():
    return sys.argv


def preinit_PIL():
    """
    This method imports several inner-PIL modules.
    It's important to run it during context initialization,
    otherwise the modules will be imported implicitly during Image.save(),
    which we do as part of sending to an image channel.

    If during such import (which takes around 0.3 sec) this process is forked,
    and the child process tries to execute this method as well, it will deadlock.

    This is not a theoretical issue - it caused a recurring problem with PyTorch data loader.
    """
    Image.preinit()
