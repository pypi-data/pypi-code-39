from collections import Iterable
from logging import getLogger
from inspect import getmodule
from ..registry import Registry

logger = getLogger(__name__)


def _get_module_path(exc_type):
    module = getmodule(exc_type)
    return f'{module.__name__}.{exc_type.__name__}'


def serialize_safe(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return {
            serialize_safe(key): serialize_safe(value[key])
            for key in value
        }
    if isinstance(value, Iterable):
        return list(map(serialize_safe, value))
    try:
        return value.__str__()
    except:
        logger.exception('Serialization failed')
        return '[serialization failed]'


def serialize_exception(exc):
    return {
        'exc_type': type(exc).__name__,
        'exc_path': _get_module_path(type(exc)),
        'exc_args': list(map(serialize_safe, exc.args)) if hasattr(exc, 'args') else None,
        'value': serialize_safe(exc),
    }


def deserialize_exception(obj, unserializable_exc_cls = Exception):
    """ Deserialize `obj` to an exception instance.

    If the `exc_path` value matches an exception registered as
    `deserializable_exception`, return an instance of that exception type.
    Otherwise, return an instance of `unserializable_exc_cls` describing the exception.
    """
    exc_type = 'Remote RPC unknown error. Data: {data}'
    value = ''
    if is_serialized_exception(obj):
        key = obj.get('exc_path')
        if key in Registry.exceptions:
            exc_args = obj.get('exc_args', ())
            return Registry.exceptions[key](*exc_args)
        exc_type = obj.get('exc_type')
        value = obj.get('value')
    else:
        try:
            exc_type = exc_type.format(data=obj)
        except:
            logger.exception('Formatting unserializable exception type failed.')
            exc_type = exc_type.format(data='?')
    return unserializable_exc_cls(f'{exc_type}{"" if not len(value) else " " + value}')


def deserializable_exception(exc_type):
    """ Decorator that registers `exc_type` as deserializable back into an
    instance, rather than a :class:`unserializable_exc_cls`. See :func:`deserialize_exception`.
    """
    key = _get_module_path(exc_type)
    Registry.exceptions[key] = exc_type
    return exc_type


def is_serialized_exception(obj) -> bool:
    return obj and type(obj) == dict and \
           'exc_path' in obj and 'exc_args' in obj and 'exc_type' in obj and 'value' in obj
