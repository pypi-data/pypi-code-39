r"""
The Trust model.
Documentation: https://api.infynity.com.au/v1/doc#!reference/trust.md
"""
from .base import InfynipyBase
from .entity.entity import ClientAccountEntity
from .entity.address import Address
from ..execeptions import ClientException


class Trust(ClientAccountEntity):

    def __init__(self, infynity, broker_id, data=None):
        """Initialize a trust instance.
        This class is intended to be interfaced with through ``infynity.broker.trust``.
        """
        super().__init__(infynity, 'trust', broker_id, data=data)

    @property
    def addresses(self):
        if not hasattr(self, 'trust_id'):
            raise ClientException('Trust does not exist.')

        endpoint = InfynipyBase.ENDPOINT + f'address/trust/{self.trust_id}'
        return [Address(d) for d in self._infynity.get(endpoint)]

    def new_address(self, address_type, data):
        if not hasattr(self, 'trust_id'):
            raise ClientException('Trust does not exist.')

        endpoint = InfynipyBase.ENDPOINT + f'address/TrustMailing/{self.trust_id}'
        self._infynity.post(endpoint, data)
