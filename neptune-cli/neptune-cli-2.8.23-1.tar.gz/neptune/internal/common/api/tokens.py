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
from collections import namedtuple
from copy import copy

import jwt

from neptune.internal.common.api.utils import REQUESTS_TIMEOUT

TOKEN_EXPIRY_MARGIN = REQUESTS_TIMEOUT + REQUESTS_TIMEOUT


class CompositeToken(object):
    def __init__(self, raw, access_token, refresh_token, raw_with_expires_at):
        self.raw = raw
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.raw_with_expires_at = raw_with_expires_at

    @classmethod
    def from_json(cls, json_token):
        access_token = _access_token_from_json(json_token[u'access_token'])
        refresh_token = _refresh_token_from_json(json_token[u'refresh_token'])
        raw_with_expires_at = cls._raw_with_expires_at(json_token, access_token)
        return CompositeToken(json_token, access_token, refresh_token, raw_with_expires_at)

    @classmethod
    def _raw_with_expires_at(cls, raw, access_token):
        # We need to set the expiry time some time earlier to avoid the situation where
        # the token expires between the check performed inside requests_oauthlib and
        # actual token validation performed when the request reaches backend.
        augmented_token = copy(raw)
        augmented_token.update({u'expires_at': access_token.expiry_time - TOKEN_EXPIRY_MARGIN})
        return augmented_token


AccessToken = namedtuple(
    'AccessToken',
    ['raw', 'expiry_time', 'issuer', 'client_name', 'roles',
     'preferred_username', 'neptune_host', 'email'])

RefreshToken = namedtuple(
    'RefreshToken',
    ['raw', 'expiry_time', 'issuer', 'client_name', 'refresh_url']
)


def _decode(json_token):
    return jwt.decode(json_token, verify=False)


def _common_token_fields(decoded_json_token):
    return decoded_json_token.get(u'exp'), decoded_json_token.get(u'iss'), decoded_json_token.get(u'azp')


def _roles(decoded_access_token):
    realm_access = decoded_access_token.get(u'realm_access')
    if realm_access:
        return realm_access.get(u'roles')
    else:
        return None


def _access_token_from_json(json_token):
    decoded_json_token = _decode(json_token)
    expiry_time, issuer, client_name = _common_token_fields(decoded_json_token)
    return AccessToken(
        raw=json_token,
        expiry_time=expiry_time,
        issuer=issuer,
        client_name=client_name,
        roles=_roles(decoded_json_token),
        preferred_username=decoded_json_token.get(u'preferred_username'),
        neptune_host=decoded_json_token.get(u'neptuneHost'),
        email=decoded_json_token.get('email')
    )


def _refresh_token_from_json(json_token):
    decoded_json_token = _decode(json_token)
    expiry_time, issuer, client_name = _common_token_fields(decoded_json_token)
    refresh_url = u"{realm_url}/protocol/openid-connect/token".format(realm_url=issuer)
    return RefreshToken(
        raw=json_token,
        expiry_time=expiry_time,
        issuer=issuer,
        client_name=client_name,
        refresh_url=refresh_url
    )
