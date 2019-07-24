r"""
Model for Client Account entity assets.
Documentation: https://api.infynity.com.au/v1/doc#!reference/asset.md
"""
from .financial import EntityFinancial


class Asset(EntityFinancial):

    def __init__(self, infynity, entity_type, entity_id, data=None):
        super().__init__(infynity, 'asset', entity_type, entity_id, data=data)
