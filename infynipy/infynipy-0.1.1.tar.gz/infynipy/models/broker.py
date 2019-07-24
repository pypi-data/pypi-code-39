r"""The Broker model, required for client account applicants"""
from .base import InfynipyBase
from .individual import Individual
from .company import Company
from .trust import Trust

from ..util import get_type
from ..exceptions import ClientException


class Broker(InfynipyBase):

    def __init__(self, infynity, broker_id):
        """Initialize a Broker instance.
        This class is intended to be interfaced with through ``infynity.broker``.
        """
        super().__init__(infynity, _data=None)

        if not isinstance(broker_id, int):
            raise ClientException(f"broker_id must be `int` not `{get_type(broker_id)}`.")

        self.broker_id = broker_id

    def _get_entities(self, entity, Model):
        """Get all entities under a broker"""
        endpoint = InfynipyBase.ENDPOINT + f'{entity}/{self.broker_id}'
        data = self._infynity.get(endpoint)

        # Return array of individuals
        return [Model(self._infynity, self.broker_id, data=d) for d in data]

    def _get_or_add_entity(self, entity, identifier, data, Model):
        """Return an existing individual or create a new one"""
        if identifier is not None:
            endpoint = InfynipyBase.ENDPOINT + f'{entity}/{self.broker_id}/{identifier}'
            data = self._infynity.get(endpoint)

        return Model(self._infynity, self.broker_id, data)

    @property
    def individuals(self):
        """Get all individuals under a broker"""
        return self._get_entities('individual', Individual)

    def individual(self, *, individual_id=None, data=None):
        """Return an existing individual or create a new one"""
        return self._get_or_add_entity('individual', individual_id, data, Individual)

    @property
    def companies(self):
        """Get all companies under a broker"""
        return self._get_entities('company', Company)

    def company(self, *, company_id=None, data=None):
        """Return an existing company or create a new one"""
        return self._get_or_add_entity('company', company_id, data, Individual)

    @property
    def trusts(self):
        """Get all trusts under a broker"""
        return self._get_entities('trust', Trust)

    def trust(self, *, trust_id=None, data=None):
        """Return an existing trust or create a new one"""
        return self._get_or_add_entity('trust', trust_id, data, Trust)
