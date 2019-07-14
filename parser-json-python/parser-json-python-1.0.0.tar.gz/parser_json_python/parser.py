from copy import deepcopy
from parser_json_python.fields import *


class Parser(object):
    """Get dict params and convert strings to Python types

    Args:
        `fields` (Field): list of fields instance that will be used for parsing params

    Methods:
        `convert_field`: use it when you need to convert one param
        `convert`: use it when you need to convert all values of dict

    Usage:
        ```
        params_input = {
            'int': '10',                     # to 10
            'float': '10.1',                 # to 10.1
            'list_field': '1,2,3',           # to ['1', '2', '3']
            'date_field': '2000-01-01 10:00' # to datetime(year=2000, month=1, day=1, hour=10, minute=0)
        }

        parser = Parser(
            fields=(FieldInt(), FieldFloat(), FieldList(), FieldDate())
        )

        params_output = parser.convert(params_input)
        ```

    """
    def __new__(cls, *args, **kwargs):
        if not getattr(cls, 'instance', None):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, fields):
        self.fields = fields

    def parse_field(self, value, field_name=None):
        for field in self.fields:
            if field.is_valid(value=value, field_name=field_name):
                return field.convert(value, field_name)

    def parse(self, params: dict):
        params = deepcopy(params)
        for field_name, value in params.items():
            params[field_name] = self.parse_field(value, field_name)
        return params


DefaultParser = Parser(
    fields=(FieldInt(), FieldFloat(), FieldList(), FieldDate())
)
