import abc
import re
from datetime import datetime


class Field(object):
    """Use for create a param for Parser

    Args:
        `param_start_with` (string): include the param key like `list`, `date` or `int`
                                     for case when you want to validate param via param name

    Methods:
        `convert`: convert value to necessary type
    """
    param_start_with = ''

    def _is_field(self, field_name):
        if self.param_start_with and field_name is not None:
            return field_name.startswith(f'{self.param_start_with}_')
        return True

    def _is_valid_value(self, value):
        return True

    def is_valid(self, value, field_name=None):
        return self._is_valid_value(value) and self._is_field(field_name)

    @abc.abstractmethod
    def _resolve(self, value):
        """Convert value to necessary type"""

    def convert(self, value, field_name=None):
        if self.is_valid(value, field_name):
            return self._resolve(value)
        return value


class FieldInt(Field):
    def _is_valid_value(self, value):
        return value.isdigit()

    def _resolve(self, value):
        return int(value)


class FieldFloat(Field):
    def _is_valid_value(self, value):
        return re.match(r"[-+]?\d*\.\d+", value)

    def _resolve(self, value):
        return float(value)


class FieldList(Field):
    param_start_with = 'list'
    separator = ','

    def _resolve(self, value):
        return value.split(self.separator)


class FieldDate(Field):
    param_start_with = 'date'
    date_template = '%Y-%m-%d %H:%M'

    def _is_valid_value(self, value):
        try:
            self._resolve(value)
            return True
        except ValueError:
            return False

    def _resolve(self, value):
        return datetime.strptime(value, self.date_template)
