r"""
Model for Client Account entity expenses.
Documentation: https://api.infynity.com.au/v1/doc#!reference/expense.md
"""
from .financial import EntityFinancial


class Expense(EntityFinancial):

    def __init__(self, infynity, entity_type, entity_id, data=None):
        super().__init__(infynity, 'expense', entity_type, entity_id, data=data)
