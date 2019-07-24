r"""
Model for Client Account entity liabilities.
Documentation: https://api.infynity.com.au/v1/doc#!reference/liability.md
"""
from .financial import EntityFinancial


class Liability(EntityFinancial):

    def __init__(self, infynity, entity_type, entity_id, data=None):
        super().__init__(infynity, 'liability', entity_type, entity_id, data=data)
