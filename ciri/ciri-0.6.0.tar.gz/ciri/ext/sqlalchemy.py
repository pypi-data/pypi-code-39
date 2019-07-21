from sqlalchemy.inspection import inspect as sa_inspect

from ciri import (Schema as CoreSchema,
                  PolySchema as CorePolySchema)
from ciri.core import ABCSchema as CoreABCSchema
from ciri.compat import add_metaclass


class ABCSchema(CoreABCSchema):

    @staticmethod
    def prepare_class(cls, name, bases, attrs):
        # Meta : model
        if 'Meta' in attrs and getattr(attrs['Meta'], 'model', None):
            attrs['__model__'] = getattr(attrs['Meta'], 'model') 

        return super(ABCSchema, cls).prepare_class(cls, name, bases, attrs)


    def find_fields(self, *args, **kwargs):
        super(ABCSchema, self).find_fields(*args, **kwargs)
        if getattr(self, '__model__', None):
            i = sa_inspect(self.__model__)
            props = i.columns
            for prop in props:
                print(prop.key)
                print(prop.type)
                print(prop.nullable)
                print(' ')
            raise Exception('weee')


@add_metaclass(ABCSchema)
class Schema(CoreSchema):
    pass


class PolySchema(CorePolySchema):

    pass
