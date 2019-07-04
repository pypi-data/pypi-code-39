from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import csv
import io
import json
import logging
import time
import urllib.parse

import jwt
import requests
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

from gsheetsviz.exceptions import (
    CredentialFormatException,
    InvalidSupportType,
    ExchangeCredentialException,
    InvalidRequiredValue,
    EncodeUrlException,
    ParseResponseException,
    VisualizeResponseException,
)

# Set how long this token will be valid in seconds
expires_in = 30  # Expires in 30 seconds

# Scope which use for exchange token with Google Auth
scopes = 'https://www.googleapis.com/auth/spreadsheets'

logger = logging.getLogger(__name__)

jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))


def init(credential=None):
    """
    Constructor for creating a connector for query Google Sheet with Google Visualization API
    """
    return Connector(credential)


def check_credential_format(credential: dict):
    """
    Check if credential is in a valid format
    :param credential:
    :return:
    """

    if credential.get('type') != 'service_account':
        raise CredentialFormatException('Only support for service account credential.')

    return credential.get('project_id') is not None \
           and credential.get('private_key_id') is not None \
           and credential.get('private_key') is not None \
           and credential.get('client_email') is not None \
           and credential.get('client_id') is not None \
           and credential.get('auth_uri') is not None \
           and credential.get('token_uri') is not None \
           and credential.get('auth_provider_x509_cert_url') is not None \
           and credential.get('client_x509_cert_url') is not None


def load_private_key(json_cred: dict):
    """
    Return the private key from the json credentials
    """

    return json_cred['private_key']


def create_signed_jwt(pkey: str, pkey_id: str, email: str, scope: str):
    """
    Create a Signed JWT from a service account Json credentials file
    This Signed JWT will later be exchanged for an Access Token
    """

    # Google Endpoint for creating OAuth 2.0 Access Tokens from Signed-JWT
    auth_url = "https://www.googleapis.com/oauth2/v4/token"

    issued = int(time.time())
    expires = issued + expires_in  # expires_in is in seconds

    # Note: this token expires and cannot be refreshed. The token must be recreated

    # JWT Headers
    additional_headers = {
        'kid': pkey_id,
        'alg': 'RS256',
        'typ': 'JWT'  # Google uses SHA256withRSA
    }

    # JWT Payload
    payload = {
        'iss': email,  # Issuer claim
        'sub': email,  # Issuer claim
        'aud': auth_url,  # Audience claim
        'iat': issued,  # Issued At claim
        'exp': expires,  # Expire time
        'scope': scope  # Permissions
    }

    # Encode the headers and payload and sign creating a Signed JWT (JWS)

    signed_jwt = jwt.encode(payload, pkey, algorithm="RS256", headers=additional_headers)

    return signed_jwt


def exchange_token(signed_jwt):
    """
    This function takes a Signed JWT and exchanges it for a Google OAuth Access Token
    """

    auth_url = "https://www.googleapis.com/oauth2/v4/token"

    params = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": signed_jwt
    }

    res = requests.post(auth_url, data=params)

    if res.ok:
        return res.json()['access_token'], None

    return None, res.text


class Connector(object):
    """
    This class use for initiated a connection to Google Visualization API
    """

    def __init__(self, credential=None):
        self.spreadsheet_id = None

        if isinstance(credential, dict):
            self.credential = credential
        elif isinstance(credential, str):
            try:
                if len(credential) > 5 and credential[-5:] != '.json':
                    self.credential = json.loads(credential)
                else:
                    with open(credential, 'r') as f:
                        data = f.read()

                    self.credential = json.loads(data)

            except Exception:
                raise InvalidSupportType(
                    'Credential should be in valid format -> json, dict, path_to_credential_json(with json extension).')
        elif credential is None:
            return

        is_valid = check_credential_format(self.credential)
        if not is_valid:
            raise CredentialFormatException('Credential is not in a valid format. Please re-downloading from Google.')

        private_key = load_private_key(self.credential)
        signed_jwt = create_signed_jwt(
            private_key,
            self.credential.get('private_key_id'),
            self.credential.get('client_email'),
            scopes)

        token, error = exchange_token(signed_jwt)

        if error is not None:
            raise ExchangeCredentialException('Google Auth return non-success status code: {}'.format(error))

        self.access_token = token

    def with_spreadsheet(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id

    def execute(self, query):
        if query is None:
            raise InvalidRequiredValue('Query should not be None.')

        try:
            query = urllib.parse.quote(query)
        except Exception as e:
            raise EncodeUrlException('Query can not be parse as urlencode. Error: {}'.format(e))

        if self.spreadsheet_id is None:
            raise InvalidRequiredValue(
                'Sheet ID should be set. (Found on https://docs.google.com/spreadsheets/d/<spreadsheet_id>)')

        base_path = 'https://docs.google.com/spreadsheets/d/'
        suffix = '/gviz/tq?tqx=out:csv'

        fp_with_token = base_path + self.spreadsheet_id + suffix
        viz_path = fp_with_token + '&tq=' + query

        if self.access_token is not None:
            viz_path = viz_path + '&access_token=' + self.access_token

        res = requests.get(viz_path)

        if res.ok:
            try:
                reader = csv.DictReader(io.StringIO(res.text))
                return list(reader), None
            except Exception as e:
                return None, ParseResponseException(e)

        return None, VisualizeResponseException(res.text)
