# -*- coding: utf-8 -*-

import sys
import inspect


__author__ = u"Peter Morawski"
__version__ = u"0.1.0"

_PY2 = 2
GEN_REPR_ID = u"__gen_repr"


def gen_repr():
    """
    Annotate a class of which the __repr__ method should be overridden.
    The generated __repr__ will contain all public fields of the class.

    >>> @gen_repr()
    >>> class Example(object):
    >>>     def __init__(self):
    >>>         self.name = u"Peter"

    >>> example = Example()
    >>> repr(example) # "<Example (name='Peter')>"
    """

    def decorator(target_cls):
        if not hasattr(target_cls, GEN_REPR_ID):
            setattr(target_cls, GEN_REPR_ID, True)

        def new_repr(instance):
            return _GenReprUtils.get_object_repr(target_cls, instance)

        target_cls.__repr__ = new_repr

        return target_cls

    return decorator


class _GenReprUtils(object):
    @classmethod
    def get_object_repr(cls, target_cls, instance):
        return u"<{class_name} ({fields})>".format(
            class_name=target_cls.__name__,
            fields=u", ".join(_GenReprUtils.extract_public_field_reprs(instance)),
        )

    @classmethod
    def extract_public_fields(cls, target):
        result = {}
        if not len(target.__dict__.keys()):
            return result

        for key, value in target.__dict__.items():
            if not key.startswith(u"_") and not key.startswith(u"__"):
                result[key] = value

        return result

    @classmethod
    def extract_public_field_reprs(cls, target):
        public_fields = cls.extract_public_fields(target)
        if not public_fields:
            return []

        result = []
        for key, value in public_fields.items():
            result.append(u"{}={}".format(key, cls.serialize_value(value)))

        return result

    @classmethod
    def serialize_value(cls, value):
        if sys.version_info.major == _PY2:
            if isinstance(value, unicode):
                return u"'{}'".format(value)

        if isinstance(value, str):
            return u"'{}'".format(value)

        if isinstance(value, dict):
            return u"{{{}}}".format(
                u", ".join(
                    [
                        u"{}: {}".format(
                            cls.serialize_value(key), cls.serialize_value(value)
                        )
                        for key, value in value.items()
                    ]
                )
            )

        if cls.value_is_iterable(value):
            return u"[{}]".format(
                u", ".join(cls.serialize_value(item) for item in value)
            )

        # check if the value is a class instance
        if (
            hasattr(value, u"__class__")
            and hasattr(value.__class__, u"__name__")
            and hasattr(value, u"__dict__")
            and inspect.isclass(value.__class__)
        ):
            # check if the object is annotated with gen_repr
            if hasattr(value.__class__, u"__gen_repr"):
                return repr(value)
            else:
                return cls.get_object_repr(value.__class__, value)

        return u"{}".format(value)

    @classmethod
    def value_is_iterable(cls, value):
        try:
            iter(value)
        except TypeError:
            return False

        return True
