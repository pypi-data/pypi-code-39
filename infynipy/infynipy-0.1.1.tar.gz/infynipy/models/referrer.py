r"""
Model for Referrers
Documentation: https://api.infynity.com.au/v1/doc#!reference/referrer.md
"""
from infynipy.models.base import InfynipyBase
from infynipy.exceptions import ClientException


class Referrer(InfynipyBase):

    def __init__(self, infynity, data=None):
        super().__init__(infynity, _data=data)

    def create(self):
        """Create an entity with an existing account"""
        if hasattr(self, 'referrer_id'):
            raise ClientException(f'referrer already exists, cannot create again.')

        endpoint = InfynipyBase.ENDPOINT + 'referrer'
        response = self._infynity.post(endpoint, self.to_dict())

        self._get(endpoint + '/' + response['referrer_id'])

        return response['referrer_id']

    def update(self):
        """Update an existing referrer"""
        if not hasattr(self, 'referrer_id'):
            raise ClientException('model has no referrer_id.')

        endpoint = InfynipyBase.ENDPOINT + f'referrer/{self.referer_id}'
        self._infynity.put(endpoint, self.to_dict())

    def delete(self):
        """Delete an existing referrer"""
        if not hasattr(self, 'referrer_id'):
            raise ClientException('model has no referrer_id.')

        endpoint = InfynipyBase.ENDPOINT + f'referrer/{self.referer_id}'
        self._infynity.delete(endpoint)
