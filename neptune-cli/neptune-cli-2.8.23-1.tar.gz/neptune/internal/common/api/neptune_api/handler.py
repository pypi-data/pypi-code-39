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
import os

import requests

from neptune import version
from neptune.generated.analytics.swagger_client.api_client import ApiClient as AnalyticsApiClient
from neptune.generated.analytics.swagger_client.apis.analyticscontroller_api import AnalyticscontrollerApi
from neptune.generated.swagger_client.api_client import ApiClient
from neptune.generated.swagger_client.apis.default_api import DefaultApi
from neptune.internal.common.api.neptune_api.neptune_oauth2_session import NeptuneOAuth2Session
from neptune.internal.common.api.tokens import CompositeToken
from neptune.internal.common.api.utils import (
    WithLoggedExceptions,
    WithWrappedExceptions,
    REQUESTS_TIMEOUT, WithWarningHandler)


def create_neptune_api_handler(base_api_handler):
    handler = WithLoggedExceptions(
        WithWrappedExceptions(
            WithWarningHandler(base_api_handler)
        ),
        skipped_error_codes={
            'create_experiment': [400],
            'update_experiment': [400],
            'create_project': [400]
        })

    return handler


def create_requests_client(rest_api_url, offline_token_storage_service):
    if 'http://' in rest_api_url:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    token = offline_token_storage_service.load()

    if token:
        refresh_kwargs = {'client_id': token.refresh_token.client_name}

        def save_raw_token(raw_json_token):
            offline_token_storage_service.save(CompositeToken.from_json(raw_json_token))

        return NeptuneOAuth2Session(
            client_id=token.refresh_token.client_name,
            token=token.raw_with_expires_at,
            auto_refresh_url=token.refresh_token.refresh_url,
            auto_refresh_kwargs=refresh_kwargs,
            token_updater=save_raw_token
        )
    else:
        return requests.Session()


def create_base_neptune_api_handler(rest_api_url, offline_token_storage_service):
    requests_client = create_requests_client(
        rest_api_url, offline_token_storage_service)
    api_client = ApiClient(requests_client=requests_client,
                           host=rest_api_url,
                           headers={'X-Neptune-CliVersion': version.__version__},
                           timeout=REQUESTS_TIMEOUT)
    return DefaultApi(api_client), requests_client


def create_base_neptune_api_handler_without_auth(rest_api_url):
    return DefaultApi(ApiClient(requests_client=requests.Session(), host=rest_api_url))


def create_analytics_api_handler(rest_api_url, offline_token_storage_service):
    requests_client = create_requests_client(
        rest_api_url, offline_token_storage_service)
    return AnalyticscontrollerApi(AnalyticsApiClient(requests_client=requests_client, host=rest_api_url))
