import json

class FieldExistsChecker:

    def __init__(self, data, field_name):
        self._data = data
        self._field_name = field_name
        self._result = None

    def __call__(self):
        return self.check()

    def get_name(self):
        return self._name

    def check(self):
        if self._data.get(self._field_name):
            self._result =  True
        else:
            self._result =  False

        return self._result

