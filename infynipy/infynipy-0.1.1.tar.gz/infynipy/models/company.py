r"""
The Compnay model.
Documentation: https://api.infynity.com.au/v1/doc#!reference/company.md
"""
from .base import InfynipyBase
from .entity.entity import ClientAccountEntity
from .entity.address import Address
from ..exceptions import ClientException


class Company(ClientAccountEntity):

    def __init__(self, infynity, broker_id, data=None):
        """Initialize a Company instance.
        This class is intended to be interfaced with through ``infynity.broker.company``.
        """
        super().__init__(infynity, 'company', broker_id, data=data)

    @property
    def addresses(self):
        if not hasattr(self, 'company_id'):
            raise ClientException('Company does not exist.')

        endpoint = InfynipyBase.ENDPOINT + f'address/company/{self.company_id}'
        return [Address(d) for d in self._infynity.get(endpoint)]

    def new_address(self, data):
        if not hasattr(self, 'company_id'):
            raise ClientException('Company does not exist.')

        endpoint = InfynipyBase.ENDPOINT + f'address/CompanyMailing/{self.compay_id}'
        self._infynity.post(endpoint, data)
