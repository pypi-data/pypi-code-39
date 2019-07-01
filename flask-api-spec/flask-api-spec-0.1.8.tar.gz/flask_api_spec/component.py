from datetime import datetime

import dateutil.parser as dp
from marshmallow import Schema, fields

from .value import NestedValue, Value


def transform_compatible_types(value):
    """
    value: Value
    """
    new_types = []
    for ty in value.types:
        if ty == datetime:
            new_types.append(str)
            new_types.append(lambda x: dp.parse(x))
        else:
            new_types.append(ty)
    value.original_types = value.types
    value.types = new_types
    value.refresh()
    return value


class Component(Schema):
    @classmethod
    def redefine(cls, k, v):
        cls.__dict__['_declared_fields'][k] = v

    def refine(self, schemes):
        for k, v in schemes:
            target = None
            if isinstance(v, Value):
                if v.types[0] == int:
                    target = fields.Int()
                elif v.types[0] == str:
                    target = fields.Str()
                elif v.types[0] == bool:
                    target = fields.Boolean()
                elif v.types[0] == datetime:
                    target = fields.DateTime()
                if target and v.many:
                    target = fields.List(target)

            elif isinstance(v, NestedValue):
                target = fields.Nested(
                    v.nested_class, *v.args, **v.kwargs)
                self.__class__.redefine(k, target)
            if not target:
                continue
            self.__class__.redefine(k, target)

    @classmethod
    def __toSchema(pcls, cls):
        schema = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, NestedValue):
                schema[k] = v.nested_class.__toSchemaCls()
            elif isinstance(v, Value):
                schema[k] = transform_compatible_types(v)
            if getattr(v, 'many', False):
                schema[k] = [schema[k]]
        return schema

    @classmethod
    def __toSchemaCls(cls):
        return Component.__toSchema(cls)

    @property
    def schema(self):
        if not self._schema:
            # extract to Schema
            self._schema = Component.__toSchema(self.__class__)
        return self._schema

    def __init__(self, *args, **kwargs):
        self._schema = None  # on Request

        self.args = args
        self.kwargs = kwargs

        self.refine(self.__class__.__dict__.items())
        Schema.__init__(self, *args, **kwargs)
