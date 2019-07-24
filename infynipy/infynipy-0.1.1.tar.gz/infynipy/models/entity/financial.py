r"""
Base Model for Client Account entitiy financials.
"""
from infynipy.models.base import InfynipyBase
from infynipy.exceptions import ClientException

from ..mixin import BaseMixin


class EntityFinancial(InfynipyBase, BaseMixin):

    def __init__(self, infynity, name, entity_type, entity_id, data=None):
        super().__init__(infynity, _data=data)
        self._name = name
        self.entity_type = entity_type
        self.entity_id = entity_id

    def create(self):
        """Create a new financial"""
        if hasattr(self, self.income_id):
            raise ClientException(f'{self.identifer} already exists, cannot create again.')

        endpoint = InfynipyBase.ENDPOINT + f'{self._name}/{self.entity_type}/{self.entity_id}'
        response = self._infynity.post(endpoint, self.to_dict())

        self._get(
            InfynipyBase.ENDPOINT +
            f'{self.name}/{self.entity_type}/{self.entity_id}/{response[self.identifer]}'
        )

        return response[self.identifer]

    def update(self):
        """Update a financial"""
        identifer = self.identifer
        if not hasattr(self, identifer):
            raise ClientException(f'{self._name} does not exists.')

        endpoint = InfynipyBase.ENDPOINT + f'{self._name}/{self.identifer_value}'
        self._infynity.put(endpoint, self.to_dict())

    def delete(self):
        """Delete a financial"""
        identifer = self.identifer
        if not hasattr(self, identifer):
            raise ClientException('{self._name} does not exist.')

        endpoint = InfynipyBase.ENDPOINT + f'{self._name}/{self.identifer_value}'
        self._infynity.delete(endpoint)
