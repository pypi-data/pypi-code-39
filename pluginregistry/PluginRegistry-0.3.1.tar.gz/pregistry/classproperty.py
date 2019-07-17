import functools


class classproperty:
    """
    Simple read-only class property.
    """

    def __init__(self, fget):
        self.getter = fget

    def __get__(self, instance, owner):
        return self.getter(owner)
