import pathlib

from functools import wraps as _wraps
from attr.validators import *


try:
    import numpy

    _isclose = numpy.isclose
except ImportError:
    import math

    _isclose = math.isclose


def _implies(precondition):
    """Applies another validator as a pre-condition.
    """

    def decorator(validator):
        @_wraps(validator)
        def decorated(*args, **kwargs):
            precondition(*args, **kwargs)
            validator(*args, **kwargs)

        return decorated

    return decorator


def nonzero(instance, attribute, value):
    """:raises ValueError: if ``value`` is zero (or close to).
    """
    if value == 0 or _isclose(value, 0):
        raise ValueError(f"Value {value!r} is zero")


def positive(instance, attribute, value):
    """:raises ValueError: if ``value`` is less or equal than zero (or very close to zero).
    """
    if value <= 0 or _isclose(value, 0):
        raise ValueError(f"Value {value!r} is not positive")


def path_exists(instance, attribute, value):
    path = pathlib.Path(value)

    if not path.exists():
        raise FileNotFoundError(f'Path "{path!s}" does not exist')


@_implies(path_exists)
def path_is_dir(instance, attribute, value):
    path = pathlib.Path(value)

    if not path.is_dir():
        raise NotADirectoryError(f'Path "{path!s}" is not a directory')
