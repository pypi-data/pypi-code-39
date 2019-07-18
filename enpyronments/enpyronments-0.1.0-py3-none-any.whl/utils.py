import sys
from contextlib import contextmanager


class UsePath:
    """Quick class to use as a context manager when importing from a relative path. While in this manager's context,
    avoid making changes to sys.path, as this manager inserts a value at the first position on enter, and removes
    whichever element is in that position on exit.
    """

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, *args):
        sys.path.pop(0)


class Sensitive(str):
    """Flags settings as sensitive, overriding their __str__ method to make accidental disclosure more difficult
    """

    def __init__(self, obj, stars=10):
        self.obj = obj
        self.stars = stars

    def __str__(self):
        return self.mask

    def __repr__(self):
        return self.obj

    def mask(self):
        return "*" * self.stars
