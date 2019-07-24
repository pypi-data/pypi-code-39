r"""
Base Model for Client Account entities.
"""
from infynipy.models.base import InfynipyBase
from infynipy.execeptions import ClientException

from .expense import Expense
from .liability import Liability
from .asset import Asset


class ClientAccountEntity(InfynipyBase):

    def __init__(self, infynity, name, broker_id, data=None):
        super().__init__(infynity, _data=data)
        self._name = name
        self.broker_id = broker_id

    def create_new_account(self, data):
        """Create an entity with a new account"""
        if hasattr(self, self.identifier):
            raise ClientException(f'{self._name} already exists, cannot create again.')

        endpoint = InfynipyBase.ENDPOINT + f'{self._name}/{self.broker_id}'
        response = self._infynity.post(endpoint, data)

        self._get(
            InfynipyBase.ENDPOINT + f'{self.name}/{self.broker_id}/{response[self.identifer]}'
        )

        return response['account_id']

    def create_existing_account(self, account_id):
        """Create an entity with an existing account"""
        if hasattr(self, self.identifier):
            raise ClientException(f'{self._name} already exists, cannot create again.')

        endpoint = InfynipyBase.ENDPOINT + f'{self._name}/{self.broker_id}/{account_id}'
        response = self._infynity.post(endpoint, self.to_dict())

        self._get(response[self.identifer])

        return response['account_id']

    def update(self):
        """Create an existing entity"""
        if self.data is None:
            raise ClientException(f'{self._name} has no fields')

        endpoint = InfynipyBase.ENDPOINT + f'{self._name}/{self.broker_id}/{self.identifier_value}'
        self._infynity.put(endpoint, self.to_dict())

    def delete_all(self):
        """Delete entity in all client accounts"""
        endpoint = InfynipyBase.ENDPOINT + f'{self._name}/{self.identifier_value}'
        self._infynity.delete(endpoint)

    def delete_account(self, account_id):
        """Delete entity in single client account"""
        endpoint = InfynipyBase.ENDPOINT + f'{self._name}/{self.identifier_value}/{account_id}'
        self._infynity.delete(endpoint)

    def _get_financials(self, name, Model):
        endpoint = InfynipyBase.ENDPOINT + f'{name}/{self._name}/{self.identifer_value}'

        return [
            Model(self._infynity, self._name, self.identifer_value, d)
            for d in self._infynity.get(endpoint)
        ]

    def _get_or_create_financial(self, name, identifer, data, Model):
        if identifer is not None:
            endpoint = InfynipyBase.ENDPOINT + f'{name}/{self._name}/{identifer}'
            data = self._infynity.get(endpoint)

        return Model(self._infynity, self._name, self.identifer_value, data)

    @property
    def expenses(self):
        return self._get_financials('expense', Expense)

    def expense(self, *, income_id=None, data=None):
        """Get an existing expense or create a new one"""
        return self._get_or_create_financial('expense', income_id, data, Liability)

    @property
    def liabilities(self):
        return self._get_financials('liability', Expense)

    def liability(self, *, liability_id=None, data=None):
        """Get an existing liability or create a new one"""
        return self._get_or_create_financial('liability', liability_id, data, Liability)

    @property
    def assets(self):
        return self._get_financials('asset', Expense)

    def asset(self, *, asset_id=None, data=None):
        """Get an existing asset or create a new one"""
        return self._get_or_create_financial('asset', asset_id, data, Asset)
