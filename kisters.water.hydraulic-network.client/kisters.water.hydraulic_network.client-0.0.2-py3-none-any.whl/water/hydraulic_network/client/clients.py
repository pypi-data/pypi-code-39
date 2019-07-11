import json

import requests

from . import AuthenticationError


class RESTClient:
    def __init__(self, url, authentication=None):
        self._url = "{}/rest/networks".format(url.rstrip("/"))
        self._authentication = authentication

    @property
    def url(self):
        return self._url

    def get(self, network_name, resource, parameters):
        url = f"{self.url}/{network_name}/{resource}"
        headers = {}
        if self._authentication:
            headers["Authorization"] = self._authentication.get_auth_header()
        resp = requests.get(url, params=parameters, headers=headers)
        if not resp.ok:
            if resp.status_code == 401:
                raise AuthenticationError(resp.text)
            raise ValueError(resp.text)
        return resp.json()

    def put(self, network_name, data):
        url = f"{self.url}/{network_name}"
        headers = {"Content-Type": "application/json"}
        if self._authentication:
            headers["Authorization"] = self._authentication.get_auth_header()
        resp = requests.put(url, data=json.dumps(data), headers=headers)
        if not resp.ok:
            if resp.status_code == 401:
                raise AuthenticationError(resp.text)
            raise ValueError(resp.text)

    def post(self, network_name, resource, data):
        url = f"{self.url}/{network_name}/{resource}"
        headers = {"Content-Type": "application/json"}
        if self._authentication:
            headers["Authorization"] = self._authentication.get_auth_header()
        resp = requests.post(url, data=json.dumps(data), headers=headers)
        if not resp.ok:
            if resp.status_code == 401:
                raise AuthenticationError(resp.text)
            raise ValueError(resp.text)

    def delete(self, network_name, resource=None, document_id=None):
        url = f"{self.url}/{network_name}"
        headers = {}
        if self._authentication:
            headers["Authorization"] = self._authentication.get_auth_header()
        if resource:
            url += "/{}".format(resource)
            if document_id:
                url += "/{}".format(document_id)
        resp = requests.delete(url, headers=headers)
        if not resp.ok:
            if resp.status_code == 401:
                raise AuthenticationError(resp.text)
            raise ValueError(resp.text)
