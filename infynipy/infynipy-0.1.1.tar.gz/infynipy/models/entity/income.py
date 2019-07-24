r"""
Model for Client Account entity incomes.
Documentation: https://api.infynity.com.au/v1/doc#!reference/income.md
"""
from infynipy.models.base import InfynipyBase
from infynipy.exceptions import ClientException

from .financial import EntityFinancial


class Income(EntityFinancial):

    def __init__(self, infynity, entity_id, data=None):
        super().__init__(infynity, 'income', 'individual', entity_id, data=data)

    def create(self):
        """Create a new financial"""
        if hasattr(self, self.income_id):
            raise ClientException(f'income already exists, cannot create again.')

        endpoint = InfynipyBase.ENDPOINT + f'income/{self.entity_type}/{self.entity_id}'
        response = self._infynity.post(endpoint, self.to_dict())

        self._get(
            InfynipyBase.ENDPOINT +
            f'income/individual/{response[self.identifer]}'
        )

        return response[self.identifer]
