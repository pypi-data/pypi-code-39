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
from future.builtins import input
from future.utils import raise_from

import base64
import json
import socketserver
import sys
from threading import Thread

from flask import Flask, request

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.framework import Command
from neptune.internal.cli.commands.neptune_command import NeptuneCommand
from neptune.internal.common import NeptuneException, NeptuneInternalException
from neptune.internal.common.api.api_service_factory import create_services
from neptune.internal.common.exceptions.keycloak_exceptions import KeycloakException
from neptune.internal.common.threads.neptune_future import NeptuneFuture


class NeptuneLogout(Command):
    name = u'logout'

    LOGGED_OUT_MESSAGE = u'You have been successfully logged out.'

    def __init__(self, token_storage):
        self.token_storage = token_storage

    def run(self, *_):
        if self.token_storage.contains_token():
            self.token_storage.clear()
        print(self.LOGGED_OUT_MESSAGE)


class NeptuneManualLogin(Command):
    name = u'manual login'

    def __init__(self, config, auth_code_url, keycloak_service, token_storage,
                 api_service, webbrowser):
        self.config = config
        self.auth_code_url = auth_code_url
        self.keycloak_service = keycloak_service
        self.token_storage = token_storage
        self.api_service = api_service
        self.webbrowser = webbrowser

    def run(self, *_):
        print(u'Please follow {} to obtain authentication token.\n'.format(self.auth_code_url))
        self.webbrowser.open(self.auth_code_url)

        user_input = input(u'Authentication token: ')

        authorization_code, redirect_uri = extract_fields(decode_token(user_input))

        offline_token = self.keycloak_service.request_offline_token(
            authorization_code=authorization_code,
            redirect_uri=redirect_uri)

        self.token_storage.save(offline_token)

        services = create_services(self.token_storage)

        services.api_service.user_logged_to_cli()

        print(u'Login successful.')


class NeptuneApiToken(NeptuneCommand):
    name = u'api key'

    def __init__(self, config, api_service):
        super(NeptuneApiToken, self).__init__(CommandNames.API_TOKEN, config, api_service=api_service)

    def run(self, *_):
        print(self.api_service.get_api_token())


class NeptuneLocalLogin(NeptuneCommand):
    name = u'local login'

    def __init__(self, config, keycloak_api_service, offline_token_storage_service,
                 api_service, webbrowser):
        super(NeptuneLocalLogin, self).__init__(CommandNames.LOGIN, config, api_service=None)
        self._keycloak_api_service = keycloak_api_service
        self._offline_token_storage_service = offline_token_storage_service
        self._aborted = False
        self._stock_server_bind = socketserver.TCPServer.server_bind
        self.api_service = api_service
        self.webbrowser = webbrowser

    def run(self, args):

        webserver_port_future, authorization_code_future = self._start_webserver(
            self._keycloak_api_service.get_local_login_redirect_url()
        )
        webserver_port = webserver_port_future.wait()

        url = self._keycloak_api_service.get_request_authorization_code_url(
            redirect_uri=self._webserver_url(webserver_port))

        # Open webbrowser in the seperate thread to avoid freeze in Firefox.
        t = Thread(target=self.webbrowser.open, args=(url,))
        t.daemon = True
        t.start()

        print("Waiting for authentication, press Ctrl+C to abort...")

        authorization_code = self._wait_for_authorization_code(authorization_code_future)

        try:
            offline_token = self._request_offline_token(
                authorization_code=authorization_code,
                redirect_uri=self._webserver_url(webserver_port)
            )
        except KeycloakException as e:
            print(e.message)
            sys.exit(1)

        self._offline_token_storage_service.save(offline_token)

        services = create_services(self._offline_token_storage_service)

        # Performs operations needed to be run for a new user on his first login.
        # TODO Consider moving this API call to Keycloak.
        services.api_service.login()

        services.api_service.user_logged_to_cli()

        print('Login successful.')

    def abort(self):
        self._aborted = True

    def _start_webserver(self, login_redirect_address):
        app = Flask(__name__)

        webserver_port_future = self._intercept_server_port()
        authorization_code_future = NeptuneFuture()

        app.add_url_rule(
            rule='/',
            endpoint='_authorization_code_request_handler',
            view_func=self._authorization_code_request_handler(authorization_code_future, login_redirect_address)
        )

        webserver_port = Thread(target=app.run, kwargs={"port": 0})
        webserver_port.setDaemon(True)
        webserver_port.start()

        return webserver_port_future, authorization_code_future

    def _wait_for_authorization_code(self, authorization_code_future):
        while not self._aborted:
            authorization_code = authorization_code_future.wait(timeout=1)
            if authorization_code:
                return authorization_code

    def _request_offline_token(self, authorization_code, redirect_uri):
        offline_token = self._keycloak_api_service.request_offline_token(
            authorization_code=authorization_code,
            redirect_uri=redirect_uri
        )
        return offline_token

    def _authorization_code_request_handler(self, authorization_code_future, login_redirect_address):
        def handler():
            authorization_code_future.set(request.args['code'])
            request.environ.get('werkzeug.server.shutdown')()

            return '<script type="text/javascript">' \
                   'window.location.href = "{frontend_address}";' \
                   '</script>'.format(frontend_address=login_redirect_address)

        return handler

    def _intercept_server_port(self):
        websocket_port_future = NeptuneFuture()

        def _server_bind_wrapper(tcp_server):
            return_value = self._stock_server_bind(tcp_server)
            websocket_port_future.set(tcp_server.socket.getsockname()[1])
            socketserver.TCPServer.server_bind = self._stock_server_bind
            return return_value

        socketserver.TCPServer.server_bind = _server_bind_wrapper

        return websocket_port_future

    def _webserver_url(self, webserver_port):
        return 'http://localhost:{}'.format(webserver_port)


def decode_token(string):
    try:
        raw_message = base64.b64decode(string)
        return json.loads(raw_message.decode('UTF-8'))
    except:
        raise NeptuneException('Invalid authentication token.')


def extract_fields(message):
    try:
        redirect_uri = message['redirect_uri']
        authorization_code = message['code']
    except KeyError as error:
        raise_from(NeptuneInternalException('Invalid JSON received from frontend.'), error)

    return authorization_code, redirect_uri
