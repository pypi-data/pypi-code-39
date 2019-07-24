"""
Settings class
"""

import os
from collections.abc import MutableMapping

from enpyronments.utils import Sensitive


class Settings(MutableMapping):
    """Holder object for settings."""

    def __init__(self, iterable=None, **kwargs):
        """ Emulate dict.__init__'s style of accepting either an iterable of pairs or a set of keyword arguments """
        if kwargs:
            self.data = dict(**kwargs)
        elif iterable:
            self.data = dict(iterable)
        else:
            self.data = dict()

    def masked(self):
        return dict(
            zip(
                self.data.keys(),
                (
                    v.mask() if isinstance(v, Sensitive) else v
                    for v in self.values(extract_from_sensitive=False)
                ),
            )
        )

    def extract_from_sensitive(self, val, extract=True):
        if extract and isinstance(val, Sensitive):
            return val.obj
        return val

    def __getitem__(self, key, extract_from_sensitive: bool = True):
        """ same as dict.__getitem__, but extracts the value of Sensitive type elements """
        val = self.data.__getitem__(key)
        return self.extract_from_sensitive(val, extract_from_sensitive)

    def __getattr__(self, key):
        """ Attempts to return attributes set on self first, then on self.data """
        try:
            return self.extract_from_sensitive(self.data[key])
        except KeyError:
            raise KeyError(
                f'"{key}" was not found in specified settings and is not an attribute of {repr(self)}.'
            )

    def __setitem__(self, key, val):
        """ Same as dict.__setitem__, but sets the value of Sensitive type elements if the current value is already
        Sensitive """
        # Don't want to set a Sensitive value to a nonsensitive value, so if:
        # 1- The key we're setting is already set
        # 2- The value we already have is sensitive
        # 3- The value we're setting isn't already sensitive
        # Then we need to wrap val in Sensitive().

        if (
            key in self.data
            and isinstance(self.get(key, extract_from_sensitive=False), Sensitive)
            and not isinstance(val, Sensitive)
        ):
            return self.data.__setitem__(key, Sensitive(val))
        return self.data.__setitem__(key, val)

    def __delitem__(self, key):
        """ Same as dict.__delitem__ """
        return self.data.__delitem__(key)

    def __iter__(self):
        """ Same as dict.__iter__ """
        return self.data.__iter__()

    def __len__(self):
        """ Same as dict.__len__ """
        return self.data.__len__()

    def get(self, key, default=None, extract_from_sensitive: bool = True):
        """ Same as dict.get, but extracts the value of Sensitive type elements """
        val = self.data.get(key)
        return self.extract_from_sensitive(val, extract_from_sensitive)

    def items(self, extract_from_sensitive: bool = True) -> tuple:
        """ Same as dict.items, but extracts the value of Sensitive type elements """
        for key, val in self.data.items():
            if extract_from_sensitive and isinstance(val, Sensitive):
                yield key, val.obj
            yield key, val

    def values(self, extract_from_sensitive: bool = True) -> tuple:
        """ Same as dict.values, but extracts the value of Sensitive type elements """
        for val in self.data.values():
            if extract_from_sensitive and isinstance(val, Sensitive):
                yield val.obj
            yield val

    def keys(self):
        return self.data.keys()

    def save_to_environ(self):
        """Saves the current state of settings to the environment via os.environ"""
        os.environ.update(self.data)
