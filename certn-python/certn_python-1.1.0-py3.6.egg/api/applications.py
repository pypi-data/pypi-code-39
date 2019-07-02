from certn.api.api import API
import json


class Applications(API):

    path = '/api/v2/applications'

    def invite(self, body):
        '''Send an email invitation to start an application'''

        return Application(
            self.client.post(f'{self.path}/invite/', data=body), api=self
        )

    def quick(self, body):
        '''Quick Application submission returns an unfinished application'''
        return Application(
            self.client.post(f'{self.path}/quick/', data=body), api=self
        )


class Application:
    def __init__(self, response, api):
        self._data = response
        self._api = api

    def __str__(self):
        return json.dumps(self._data, sort_keys=True, indent=4)

    @property
    def data(self):
        return self._data

    @property
    def id(self):
        return self._data.get('id')

    @property
    def status(self):
        return self._data.get('status')

    def get(self, value, default=None):
        return self._data.get(value, default)
