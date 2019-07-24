r"""
The Address model.
Documentation: https://api.infynity.com.au/v1/doc#!reference/address.md
"""
from infynipy.models.base import InfynipyBase
from infynipy.exceptions import ClientException


class Address(InfynipyBase):

    def __init__(self, infynity, data=None):
        """Initialize an Address instance.
        This class is intended to be interfaced with through ``infynity.broker.{entity}.address``.
        """
        super().__init__(infynity, _data=data)

    def update(self):
        """Update an existing address"""
        if not hasattr(self, 'address_id'):
            raise ClientException('model has no address_id')

        endpoint = InfynipyBase.ENDPOINT + f'addresss/{self.address_id}'
        self._infynity.put(endpoint, self.to_dict())

    def delete(self):
        """Delete an existing address"""
        if not hasattr(self, 'address_id'):
            raise ClientException('model has no address_id.')

        endpoint = InfynipyBase.ENDPOINT + f'addresss/{self.address_id}'
        self._infynity.delete(endpoint)
