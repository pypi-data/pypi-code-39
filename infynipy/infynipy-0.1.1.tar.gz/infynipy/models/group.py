r"""
Model for Referrer Groups
Documentation: https://api.infynity.com.au/v1/doc#!reference/referrergroup.md
"""
from infynipy.models.base import InfynipyBase
from infynipy.exceptions import ClientException


class ReferrerGroup(InfynipyBase):

    def __init__(self, infynity, data=None):
        super().__init__(infynity, _data=data)

    def create(self):
        """Create an entity with an existing account"""
        if hasattr(self, 'group_id'):
            raise ClientException(f'group already exists, cannot create again.')

        endpoint = InfynipyBase.ENDPOINT + 'referrergroup'
        response = self._infynity.post(endpoint, self.to_dict())

        self._get(endpoint + '/' + response['group_id'])

        return response['group_id']

    def update(self):
        """Update an existing group"""
        if not hasattr(self, 'group_id'):
            raise ClientException('model has no group_id.')

        endpoint = InfynipyBase.ENDPOINT + f'referrergroup/{self.referer_id}'
        self._infynity.put(endpoint, self.to_dict())

    def delete(self):
        """Delete an existing group"""
        if not hasattr(self, 'group_id'):
            raise ClientException('model has no group_id.')

        endpoint = InfynipyBase.ENDPOINT + f'referrergroup/{self.referer_id}'
        self._infynity.delete(endpoint)
