"""




AI Fashion API SDK

af oauth2


"""


import os
import time
from enum import Enum
import json
import yaml
import requests


AF_CLIENT_ID_SECRET_FNAME = 'client_keys.yaml'
AF_CLIENT_ID_SECRET_FNAME = os.path.expanduser(os.path.join('~', AF_CLIENT_ID_SECRET_FNAME))


class OAuth2GrandTypes(Enum):
    """docstring for OAuth2GrandTypes"""
    authorization_code = 10 # more secure
    client_credentials = 20 # more speed





class AFOAuth2():
    """docstring for AFToken"""
    Endpoint = {
        OAuth2GrandTypes.authorization_code : "https://api.aifashion.com/oauth2/authorize",
        OAuth2GrandTypes.client_credentials : "https://api.aifashion.com/oauth2/token",
    }
    TOKEN_URL = "https://api.aifashion.com/oauth2/token"

    def __init__(self, client_id=None, client_secret=None, client_filename=None,
                 grant_type=OAuth2GrandTypes.client_credentials, check=True, timeout=2, debug=False):
        super(AFOAuth2, self).__init__()
        if client_id and client_secret:
            self.client_id = client_id
            self.client_secret = client_secret
        elif client_filename:
            self.__get_client_id_secret_from_file__(client_filename)
        self.grant_type = grant_type
        if check:
            self.__check_oauth2_validity__()
        self.timeout = timeout
        self.debug = debug
        self._token_data = None


    def __get_client_id_secret_from_file__(self, client_filename):
        """
        read a yaml file storing client_id and client_secret
        if client_filename is given
        """
        fnames = [os.path.realpath(client_filename),
                  AF_CLIENT_ID_SECRET_FNAME]
        for fname in fnames:
            if os.path.exists(fnames):
                with open(fname) as fd:
                    data_map = yaml.safe_load(fd)
                    assert 'client_id' in data_map and 'client_secret' in data_map, \
                        '{0} does not contain client_id and client_secret'.format(fname)
                    self.client_id, self.client_secret = \
                        data_map['client_id'], data_map['client_secret']


    def __check_oauth2_validity__(self):
        """
        check the validity of client_id and client_secret
        """
        assert isinstance(self.client_id, str) and isinstance(self.client_secret, str), \
            'client_id and client_secret should be string'
        assert self.grant_type == OAuth2GrandTypes.authorization_code or \
            self.grant_type == OAuth2GrandTypes.client_credentials, \
            'grant_type should be a enumerate of OAuth2GrandTypes'


    @property
    def token(self):
        """
        Automatically get a token using client_id & client_secret
        """
        if not (hasattr(self, "_token_data") and self._token_data) or self.token_expired:
            self.request_token()
        return self._token_data['access_token']


    def request_token(self):
        """
        request a token using requests POST
        """
        required_time = time.time()
        payload = "grant_type={0}&client_id={1}&client_secret={2}".format(\
                    self.grant_type.name, self.client_id, self.client_secret)
        headers = {
            'content-type': "application/x-www-form-urlencoded"
        }
        url = self.TOKEN_URL
        response = requests.request("POST", url, data=payload, headers=headers,
                                    timeout=self.timeout)
        self._token_data = json.loads(response.text)
        self._token_data.update({
            'required_time' : required_time,
            })
        # return response['access_token']


    @property
    def token_expired(self):
        """
        Check if token is expired
        10 seconds for cache
        """
        if hasattr(self, '_token_data'):
            required_time = self._token_data['required_time']
            expires_in = self._token_data['expires_in']
            time_now = time.time()
            if time_now - required_time > expires_in - 10:
                return True
        return False
