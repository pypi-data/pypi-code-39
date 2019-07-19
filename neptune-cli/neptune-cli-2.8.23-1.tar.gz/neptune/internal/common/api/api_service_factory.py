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

from collections import namedtuple
import json
import logging
import os
import sys

from future.builtins import object

from neptune.internal.cli.commands.utils.urls import Urls
from neptune.internal.cli.helpers import should_retry_api_calls
from neptune.internal.common.api import OfflineTokenStorageService
from neptune.internal.common.api.address import Address, \
    rest_url_from_address
from neptune.internal.common.api.analytics_api_service import AnalyticsApiService
from neptune.internal.common.api.job_api_service import JobApiService
from neptune.internal.common.api.neptune_api.handler import create_analytics_api_handler, \
    create_base_neptune_api_handler, create_base_neptune_api_handler_without_auth, create_neptune_api_handler
from neptune.internal.common.api.tokens import CompositeToken
from neptune.internal.common.api.utilities_api_service import UtilitiesService
from neptune.internal.common.config.host_parser import HostParser, PortParser, SecureParser
from neptune.server import __analytics_api__ as analytics_api

Services = namedtuple(
    'Services',
    ['api_service', 'utilities_service', 'session'])

LOG_IN_MESSAGE = u'You need to log in using `neptune account login`.'


def create_services(offline_token_storage_service):
    token = offline_token_storage_service.load()

    if not token:
        print(LOG_IN_MESSAGE)
        return

    neptune_host = token.access_token.neptune_host

    if not neptune_host:
        offline_token_storage_service.clear()
        print(LOG_IN_MESSAGE)
        return

    _address = Address(HostParser().parse(neptune_host), PortParser().parse(neptune_host))
    _secure = SecureParser().parse(neptune_host) == 'https'

    if not _secure:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    api_service_factory = ApiServiceFactory(
        urls=Urls(rest_url_from_address(_address, _secure)),
        offline_token_storage_service=offline_token_storage_service,
        with_retries=should_retry_api_calls()
    )
    return api_service_factory.create_services()


def setup_offline_token_storage_service(local_storage):

    token = os.environ.get('NEPTUNE_TOKEN')

    if token:
        token = CompositeToken.from_json(json.loads(token, encoding='UTF-8'))

    return OfflineTokenStorageService.create(
        token_dirpath=local_storage.tokens_directory.absolute_path, token=token)


def create_analytics_service(offline_token_storage_service):
    token = offline_token_storage_service.load()
    if not token:
        return None

    neptune_host = token.access_token.neptune_host

    if "app.neptune.ml" not in neptune_host and os.getenv("USE_EXTERNAL_APIS", None) is None:
        return None

    _address = Address(HostParser().parse(neptune_host), PortParser().parse(neptune_host))
    _secure = SecureParser().parse(neptune_host) == 'https'

    if not _secure:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    urls = Urls(rest_url_from_address(_address, _secure))
    base_api_handler_with_auth = create_analytics_api_handler(
        urls.rest_api_url + "/" + analytics_api, offline_token_storage_service)

    return AnalyticsApiService(base_api_handler_with_auth)


def send_neptune_crash(exc, local_storage):
    try:
        offline_token_storage_service = setup_offline_token_storage_service(local_storage)
        analytics = create_analytics_service(offline_token_storage_service)
        if analytics:
            analytics.send_neptune_crash(exc)
    except Exception as e:
        logging.getLogger(__name__).debug('Unable to initialize analytics service: %s', str(e))


def install_analytics_sys_hook(local_storage):
    __excepthook__ = sys.excepthook

    def handle_exception(*exc_info):
        send_neptune_crash(exc=exc_info[1], local_storage=local_storage)
        __excepthook__(*exc_info)

    sys.excepthook = handle_exception


class ApiServiceFactory(object):
    def __init__(self, urls, offline_token_storage_service, with_retries=True):
        self._urls = urls
        self._offline_token_storage_service = offline_token_storage_service
        self._default_with_retries = with_retries

    def create_services(self, with_retries=None):
        base_api_handler_with_auth, requests_client_with_auth = create_base_neptune_api_handler(
            self._urls.rest_api_url, self._offline_token_storage_service)
        base_api_handler_without_auth = \
            create_base_neptune_api_handler_without_auth(self._urls.rest_api_url)

        neptune_api_handler_with_auth = create_neptune_api_handler(base_api_handler_with_auth)
        neptune_api_handler_without_auth = create_neptune_api_handler(base_api_handler_without_auth)

        utilities_service = UtilitiesService(
            neptune_api_handler_with_auth,
            neptune_api_handler_without_auth
        )

        retries_enabled = with_retries if with_retries is not None else self._default_with_retries

        api_service = JobApiService(
            urls=self._urls,
            requests_client=requests_client_with_auth,
            neptune_api_handler=neptune_api_handler_with_auth,
            retries_enabled=retries_enabled,
            utilities_service=utilities_service
        )

        return Services(api_service, utilities_service, requests_client_with_auth)
