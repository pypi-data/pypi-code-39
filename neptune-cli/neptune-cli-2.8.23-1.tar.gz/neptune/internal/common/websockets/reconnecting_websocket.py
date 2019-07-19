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

from __future__ import print_function

import logging

from future.builtins import object
from websocket import WebSocketTimeoutException, WebSocketConnectionClosedException

from neptune.internal.common.api.utils import MAX_RETRY_DELAY
from neptune.internal.common.exceptions.base_exceptions import NeptuneThreadInterruptedException
from neptune.internal.common.sentry import get_sentry_client_instance
from neptune.internal.common.utils.time import compute_delay
from neptune.internal.common.websockets.websocket_client_adapter import WebsocketClientAdapter, \
    WebsocketNotConnectedException

CONNECTION_LOST_MESSAGE = u"Websocket connection lost. Retrying..."
CONNECTION_RESTORED_MESSAGE = u"Websocket connection restored!"


class ReconnectingWebsocket(object):
    def __init__(self, url, offline_token_storage_service, keycloak_api_service, shutdown_event, local_storage):
        self.url = url
        self.client = WebsocketClientAdapter()
        self._logger = logging.getLogger(__name__)
        self._shutdown_event = shutdown_event
        self._offline_token_storage_service = offline_token_storage_service
        self._keycloak_api_service = keycloak_api_service
        self._token = self._offline_token_storage_service.load()
        self._reconnect_counter = ReconnectCounter()
        self._local_storage = local_storage

    def shutdown(self):
        self._shutdown_event.set()
        self.client.abort()
        self.client.shutdown()

    def recv(self):
        if not self.client.connected:
            self._try_to_establish_connection()
        while self._is_active():
            try:
                data = self.client.recv()
                self._on_successful_connect()
                return data
            except WebSocketTimeoutException:
                raise
            except WebSocketConnectionClosedException:
                if self._is_active():
                    self._handle_lost_connection(report_exception_to_sentry=False)
                else:
                    raise NeptuneThreadInterruptedException()
            except WebsocketNotConnectedException:
                if self._is_active():
                    self._handle_lost_connection(report_exception_to_sentry=False)
            except Exception:
                if self._is_active():
                    self._handle_lost_connection(report_exception_to_sentry=True)

    def _is_active(self):
        return not self._shutdown_event.is_set()

    def _on_successful_connect(self):
        if self._reconnect_counter.retries >= 1:
            print(CONNECTION_RESTORED_MESSAGE)
            self._logger.info("Established connection to %s in #%d attempt.",
                              self.url, self._reconnect_counter.retries)
        self._reconnect_counter.clear()

    def _try_to_establish_connection(self):
        try:
            self._request_token_refresh()
            if self.client.connected:
                self.client.shutdown()
            self.client.connect(url=self.url, token=self._token)
        except Exception:
            get_sentry_client_instance(self._local_storage).send_exception()
            self._shutdown_event.wait(self._reconnect_counter.calculate_delay())

    def _handle_lost_connection(self, report_exception_to_sentry):
        print(CONNECTION_LOST_MESSAGE)
        if report_exception_to_sentry:
            get_sentry_client_instance(self._local_storage).send_exception()
        self._reconnect_counter.increment()
        self._try_to_establish_connection()

    def _request_token_refresh(self):
        self._token = self._keycloak_api_service.request_token_refresh(self._token.refresh_token)
        self._offline_token_storage_service.save(self._token)


class ReconnectCounter(object):
    def __init__(self):
        self.retries = 0

    def clear(self):
        self.retries = 0

    def increment(self):
        self.retries += 1

    def calculate_delay(self):
        return compute_delay(self.retries, MAX_RETRY_DELAY)
