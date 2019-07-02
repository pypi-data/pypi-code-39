from certn.api.api import API
import json


class Properties(API):

    path = '/api/v2/properties'

    def list(self):
        responses = self.client.get(f'{self.path}/')
        results = []
        for result in responses.get('results', []):
            results.append(Property(result, self))

        return results

    def get(self, property_id):
        return Property(self.client.get(f'{self.path}/{property_id}'), api=self)

    def add(self, data):
        return Property(self.client.post(f'{self.path}/', data), api=self)

    def update(self, property_id, data):
        return Property(
            self.client.put(f'{self.path}/{property_id}/', data), api=self
        )

    def delete(self, property_id):
        return self.client.delete(f'{self.path}/{property_id}/')


class Property:
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

    def get(self, value, default=None):
        return self._data.get(value, default)
