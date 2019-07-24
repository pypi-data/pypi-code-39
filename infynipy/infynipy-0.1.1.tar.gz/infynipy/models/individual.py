r"""
The Individual model.
Documentation: https://api.infynity.com.au/v1/doc#!reference/individual.md
"""
from .base import InfynipyBase
from .entity.entity import ClientAccountEntity
from .entity.address import Address
from .entity.employment import Employment
from .entity.income import Income
from ..exceptions import ClientException


class Individual(ClientAccountEntity):

    def __init__(self, infynity, broker_id, data=None):
        """Initialize an Individual instance.
        This class is intended to be interfaced with through ``infynity.broker.individual``.
        """
        super().__init__(infynity, 'individual', broker_id, data=data)

    @property
    def addresses(self):
        if not hasattr(self, 'individual_id'):
            raise ClientException('Individual does not exist.')

        endpoint = InfynipyBase.ENDPOINT + f'address/individual/{self.individual_id}'
        return [Address(d) for d in self._infynity.get(endpoint)]

    def new_address(self, address_type, data):
        if not hasattr(self, 'individual_id'):
            raise ClientException('Individual does not exist.')

        endpoint = InfynipyBase.ENDPOINT + f'address/{address_type}/{self.individual_id}'
        self._infynity.post(endpoint, data)

    @property
    def employments(self):
        """Get all employments."""
        endpoint = InfynipyBase.ENDPOINT + f'employment/all/{self.individual_id}'
        return [Employment(d, self.individual_id) for d in self._infynity.get(endpoint)]

    def employment(self, *, employment_id=None, data=None):
        """Get an existing employment or create a new one"""
        if employment_id is not None:
            endpoint = InfynipyBase.ENDPOINT + f'employment/{employment_id}'
            data = self._infynity.get(endpoint)

        return Employment(self._infynity, self.individual_id, data)

    @property
    def incomes(self):
        """Get all incomes."""
        endpoint = InfynipyBase.ENDPOINT + f'income/individual/{self.individual_id}'
        return [Income(d, self.individual_id) for d in self._infynity.get(endpoint)]

    def income(self, *, income_id=None, data=None):
        """Get an existing employment or create a new one"""
        if income_id is not None:
            endpoint = InfynipyBase.ENDPOINT + f'income/{income_id}'
            data = self._infynity.get(endpoint)

        return Income(self._infynity, self.individual_id, data)
