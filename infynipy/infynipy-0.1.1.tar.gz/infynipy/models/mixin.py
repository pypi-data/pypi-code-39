r"""
Some base classes (EntityFinacial, ClientAccountEntity) use these values.
"""


class BaseMixin:

    @property
    def identifer(self):
        return self._name + '_id'

    @property
    def identifer_value(self):
        identifier = self.identifer
        return getattr(self, identifier)
