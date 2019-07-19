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
from future.utils import raise_from

import logging

import requests
from requests.exceptions import RequestException

from neptune.internal.common.api.address import Address, http_url_from_address
from neptune.internal.common.api.neptune_api.handler import REQUESTS_TIMEOUT
from neptune.internal.common.api.tokens import CompositeToken
from neptune.internal.common.config.host_parser import HostParser, PortParser, SecureParser
from neptune.internal.common.exceptions.keycloak_exceptions import KeycloakException


class KeycloakApiService(object):
    def __init__(self, config):
        self._logger = logging.getLogger(__name__)
        self.config = config

    def get_request_authorization_code_url(self, redirect_uri):
        self._validate_login_url()
        return (
            "{realm_url}/protocol/openid-connect/auth"
            "?client_id={client_id}&redirect_uri={redirect_uri}"
            "&response_type=code&scope=offline_access"
        ).format(
            realm_url=self.config.realm_url,
            client_id=self.config.client_id,
            redirect_uri=redirect_uri
        )

    def get_local_login_redirect_url(self):
        self._validate_login_url()
        return self.config.local_login_redirect_url

    def request_offline_token(self, authorization_code, redirect_uri):
        """ Redirect URI is required because of security reasons. No redirect is performed.  """

        offline_token_request_body = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "redirect_uri": redirect_uri,
            "code": authorization_code
        }

        result = self._post(self.config.token_url, offline_token_request_body)

        return CompositeToken.from_json(json_token=result)

    def request_token_refresh(self, refresh_token):
        token_refresh_request_body = {
            "grant_type": "refresh_token",
            "client_id": refresh_token.client_name,
            "refresh_token": refresh_token.raw
        }
        return CompositeToken.from_json(self._post(refresh_token.refresh_url, token_refresh_request_body))

    def _post(self, url, body):
        try:
            return self._try_to_post(url, body)
        except requests.exceptions.RequestException as err:
            raise_from(KeycloakException("Neptune has experienced some connection problems. Please try again."), err)

    @staticmethod
    def _try_to_post(url, body):
        response = requests.post(url, body, timeout=REQUESTS_TIMEOUT)
        if response.status_code == requests.codes.ok or response.status_code == requests.codes.bad_request: # pylint:disable=no-member
            response_json = response.json()
            if response_json.get('error'):
                if response_json.get('error') == 'invalid_grant':
                    if (response_json.get('error_description') and
                            response_json.get('error_description') == 'Client session not active'):
                        raise KeycloakException('Session has expired.')
                    else:
                        raise KeycloakException('Invalid authorization code.')
                else:
                    if response_json.get('error_description'):
                        raise KeycloakException(str(response_json.get('error_description')))
                    else:
                        raise KeycloakException('Unknown error.')
            return response_json
        else:
            raise RequestException()

    def _validate_login_url(self):
        from requests.packages import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = self.config.auth_url
        # make sure http/https is present
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        # take base domain i.e. https://neptune.ml
        url = "/".join(url.split("/")[0:3])

        # check if http/https is correct
        try:
            response = requests.get(url, allow_redirects=False, verify=False)
            if response.status_code == 301:  # http is not used/allowed
                url = response.headers['Location']
        except RequestException:
            raise KeycloakException('Unable to access auth server. Login url is incorrect')

        parts = url.split("/")

        # try accessing address directly
        # this reflects single instance deployment without auth sub-domain and ip deployment
        if KeycloakApiService._test_auth_url(url):
            self.config.auth_url = url
            return
        # try adding 'auth.' subdomain
        # this reflects single instance deployments with auth sub-domain
        if not parts[2].startswith("auth."):
            test_url = parts[0] + "//auth." + parts[2]
            if KeycloakApiService._test_auth_url(test_url):
                self.config.auth_url = test_url
                return
        # try replacing first subdomain with 'auth'
        # this reflects multi instance deployments with parallel sub-domains
        test_url = parts[0] + "//auth." + ".".join(parts[2].split(".")[1:])
        if KeycloakApiService._test_auth_url(test_url):
            self.config.auth_url = test_url
            return

        # could not verify access to login server.
        raise KeycloakException('Unable to access auth server. Login url is incorrect')

    @staticmethod
    def _test_auth_url(test_url):
        try:
            response = requests.get(test_url + '/auth/realms/neptune', allow_redirects=False, verify=False)
            return response.status_code == 200
        except RequestException:
            return False


class KeycloakApiConfig(object):
    def __init__(self, auth_url='https://auth.neptune.ml', client_id='neptune-cli'):
        self.auth_url = auth_url
        self.client_id = client_id

    def _get_base_redirect_address(self):
        auth_host = HostParser().parse(self.auth_url)
        if auth_host.startswith("auth."):
            auth_host = auth_host[5:]
        _address = Address(HostParser().parse(self.auth_url), PortParser().parse(self.auth_url))
        _address.host = auth_host
        _secure = SecureParser().parse(self.auth_url) == 'https'
        return http_url_from_address(_address, _secure)

    @property
    def redirect_url(self):
        return self._get_base_redirect_address() + '/get-cli-token'

    @property
    def local_login_redirect_url(self):
        return self._get_base_redirect_address() + '/cli-successful-login'

    @property
    def realm_url(self):
        return self.auth_url + '/auth/realms/neptune'

    @property
    def token_url(self):
        return "{realm_url}/protocol/openid-connect/token".format(realm_url=self.realm_url)

    @property
    def manual_login_url(self):
        return self.realm_url + \
               "/protocol/openid-connect/auth?client_id=neptune-cli" + \
               "&redirect_uri=" + self.redirect_url + \
               "&response_mode=fragment&" + \
               "response_type=code&scope=openid"
