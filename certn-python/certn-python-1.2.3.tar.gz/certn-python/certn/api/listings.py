from certn.api.api import API
import json


class Listings(API):

    path = '/api/v2/listings'

    def list(self):

        responses = self.client.get(f'{self.path}/')
        results = []
        for result in responses.get('results', []):
            results.append(Listing(result, self))

        return results

    def get(self, listing_id):
        return Listing(self.client.get(f'{self.path}/{listing_id}/'), api=self)

    def add(self, data):
        return Listing(self.client.post(f'{self.path}/', data), api=self)

    def update(self, listing_id, data):
        return Listing(self.client.put(f'{self.path}/{listing_id}/', data), api=self)

    def delete(self, listing_id):
        return self.client.delete(f'{self.path}/{listing_id}/')


class Listing:
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
