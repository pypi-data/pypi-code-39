import json
import requests

from .models.base import InfynipyBase
from .exceptions import APIException
from .util import JSONEncoder
from . import models


class Infynity:
    """The Infynity class provides convenient access to Infynity's API.
    Instances of this class are the gateway to interacting with Infynity's API
    through infynipy. The canonical way to obtain an instance of this class
    is via:

    .. code-block:: python
       import infynipy
       infynity = infynipy.Infynity(username='USERNAME', api_key='API_KEY')
    """

    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key

    def _parse_resp(self, resp):
        """Check if the response is an error"""
        json = resp.json()

        if isinstance(json, dict) and json.get('error'):
            raise APIException(json['error']['status'], json['error']['message'])
        else:
            return json

    def _get_data(self, data):
        return json.dumps(data, cls=JSONEncoder)

    def get(self, url):
        """Request method to get entit(y,ies)"""
        return self._parse_resp(requests.get(url, auth=(self.username, self.api_key)))

    def post(self, url, data):
        """Request method to create a new entity"""
        return self._parse_resp(
            requests.post(
                url, data=self._get_data(data), auth=(self.username, self.api_key),
                headers={'Content-Type': 'application/json'}
            )
        )

    def put(self, url, data):
        """Request method to update an entity"""
        return self._parse_resp(
            requests.put(
                url, data=self._get_data(data), auth=(self.username, self.api_key),
                headers={'Content-Type': 'application/json'}
            )
        )

    def delete(self, url):
        """Request method to delete an entity"""
        return self._parse_resp(requests.delete(url, auth=(self.username, self.api_key)))

    def broker(self, broker_id):
        return models.Broker(self, broker_id)

    @property
    def referrers(self):
        endpoint = InfynipyBase.ENDPOINT + 'referrer'
        return [models.Referrer(self, d) for d in self.get(endpoint)]

    def referrer(self, *, referrer_id=None, data=None):
        if referrer_id is not None:
            endpoint = InfynipyBase.ENDPOINT + f'referrer/{referrer_id}'
            data = self.get(endpoint)

        return models.Referrer(self, data)

    @property
    def referrer_groups(self):
        endpoint = InfynipyBase.ENDPOINT + 'referrergroup'
        return [models.ReferrerGroup(self, d) for d in self.get(endpoint)]

    def referrer_group(self, *, group_id=None, data=None):
        if group_id is not None:
            endpoint = InfynipyBase.ENDPOINT + f'referrergroup/{group_id}'
            data = self.get(endpoint)

        return models.ReferrerGroup(self, data)
