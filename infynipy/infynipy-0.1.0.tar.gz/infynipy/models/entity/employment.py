r"""
The Employment model.
Documentation: https://api.infynity.com.au/v1/doc#!reference/employment.md
"""
from infynipy.models.base import InfynipyBase
from infynipy.execeptions import ClientException


class Employment(InfynipyBase):

    def __init__(self, infynity, individual_id, data=None):
        """Initialize an Employment instance.
        This class is intended to be interfaced with through:
        ``infynity.broker.individual.Employment``.
        """
        super().__init__(infynity, _data=data)
        self.individual_id = individual_id

    def create(self):
        if hasattr(self, 'employment_id'):
            raise ClientException('Employment has employment_id, cannot create again.')

        endpoint = InfynipyBase.ENDPOINT + f'employment/{self.individual_id}'
        response = self._infynity.post(endpoint, self.to_dict())

        self._get(InfynipyBase.ENDPOINT + f'employment/{response["employment_id"]}')

    def update(self):
        """Update an existing employment"""
        if not hasattr(self, 'employment_id'):
            raise ClientException('No employment_id.')

        endpoint = InfynipyBase.ENDPOINT + f'employment/{self.employment_id}'
        self._infynity.put(endpoint, self.to_dict())

    def delete(self):
        """Delete an existing employment"""
        if not hasattr(self, 'employment_id'):
            raise ClientException('No employment_id.')

        endpoint = InfynipyBase.ENDPOINT + f'addresss/{self.employment_id}'
        self._infynity.delete(endpoint)
