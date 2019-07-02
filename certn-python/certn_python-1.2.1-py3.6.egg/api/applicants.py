from certn.api.api import API
import json


class Applicants(API):

    path = '/api/v2/applicants'

    def get(self, application_id):
        '''Get the application for a given application_id'''
        return Applicant(self.client.get(f'{self.path}/{application_id}/'), api=self)

    def delete(self, application_id):
        '''delete the application for a given application_id'''
        return self.client.delete(f'{self.path}/{application_id}/')

    def list(self):
        '''Get the applicant lists'''
        responses = self.client.get(f'{self.path}/')
        results = []
        for result in responses.get('results', []):
            results.append(Applicant(result, self))

        return results


class Applicant:
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
