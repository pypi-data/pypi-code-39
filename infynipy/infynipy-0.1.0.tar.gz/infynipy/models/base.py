r"""The InfynipyBase superclass"""


class InfynipyBase:

    ENDPOINT = 'https://api.infynity.com.au/v1/'
    # ENDPOINT = 'http://127.0.0.1:5000/v1/'

    def _get(self, endpoint):
        # On creates we want to get the resource again because the user may
        # not have filled in all the data.
        data = self._infynity.get(endpoint)
        self.from_dict(data)

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        for attribute, value in data.items():
            setattr(self, attribute, value)

    @classmethod
    def parse(cls, data, infynity):
        """Return an instance of ``cls`` from ``data``.
        :param data: The structured data.
        :param reddit: An instance of :class:`.Infynity`.
        """
        return cls(infynity, _data=data)

    def __init__(self, infynity, _data):
        """Initialize a InfynipyBase instance.
        :param ifnynity: An instance of :class:`.Infynity`.
        """
        self._infynity = infynity

        if _data:
            self.from_dict(_data)

    @property
    def identifer(self):
        return self._name + '_id'

    @property
    def identifer_value(self):
        identifier = self.identifer
        return getattr(self, identifier)
