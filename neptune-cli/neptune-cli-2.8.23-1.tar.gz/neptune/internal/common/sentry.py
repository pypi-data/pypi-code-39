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
import collections
import threading

from future.utils import with_metaclass
from raven import Client
from raven.transport.requests import RequestsHTTPTransport

from neptune.internal.common.api.offline_token_storage_service import OfflineTokenStorageService
from neptune.version import __version__ as cli_version

UserContext = collections.namedtuple('UserContext', ['username', 'neptune_host'])

_DSN = None


class _Singleton(type):
    _instance = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class ClientWithStorage(Client):

    def __init__(self, local_storage=None, dsn=None, transport=None, install_sys_hook=True):
        super(ClientWithStorage, self).__init__(dsn=dsn, transport=transport, install_sys_hook=install_sys_hook)
        self._local_storage = local_storage


class _SentryClient(with_metaclass(_Singleton, ClientWithStorage)):

    def send_exception(self):
        try:
            self.captureException()
        except Exception:
            pass

    def captureException(self, exc_info=None, **kwargs):
        user_context = _get_user_context(self._local_storage)
        self.user_context({
            'username': user_context.username
        })
        self.tags_context({
            'neptune_host': user_context.neptune_host,
            'cli-version': cli_version
        })
        super(_SentryClient, self).captureException(exc_info=None, **kwargs)


def install_sentry_sys_hook(local_storage):
    """
    Install sys.excepthook in sentry client on uncaught exceptions.
    Disabled by default in sentry client instance from get_sentry_client_instance().
    """
    client = get_sentry_client_instance(local_storage)
    client.install_sys_hook()


def get_sentry_client_instance(local_storage):
    try:
        client = _SentryClient(dsn=_DSN, transport=RequestsHTTPTransport, install_sys_hook=False,
                               local_storage=local_storage)
    except Exception:
        client = _SentryClient()
    return client


def _get_user_context(local_storage):
    offline_token_storage_service = OfflineTokenStorageService.create(
        token_dirpath=local_storage.tokens_directory.absolute_path)

    try:
        token = offline_token_storage_service.load()
    except Exception:
        token = None

    if token:
        return UserContext(
            username=token.access_token.preferred_username or 'unknown',
            neptune_host=token.access_token.neptune_host or 'unknown')
    else:
        return UserContext('unknown', 'unknown')
