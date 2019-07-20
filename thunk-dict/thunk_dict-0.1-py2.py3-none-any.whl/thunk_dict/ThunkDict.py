import collections.abc
import copy


class ThunkDict(collections.abc.MutableMapping):
    DICT_LIKE_EXN = TypeError("dictionary must be a dict-like object")

    class __LazyInternal__(object):
        def release(self):
            return self.value()

        def __call__(self, item):
            self.value = item
            return self

    def __init__(self, dictionary=None, *args, **kwargs):
        self.__lazy__wrapper__ = self.__LazyInternal__()
        self.__dictionary__ = None

        if isinstance(dictionary, dict):
            self.__dictionary__ = dictionary
        elif dictionary is None:
            self.__dictionary__ = {}
        else:
            raise self.DICT_LIKE_EXN

        self.__dictionary__.update(*args, **kwargs)

        self.__dictionary__ = {key: self.__thunk__(
            self.__dictionary__[key]) for key in self.__dictionary__}

    def get(self, key, fallback=None):
        if key in self:
            return self[key]
        return fallback

    def get_dict(self):
        return self.__dictionary__

    def set_dict(self, dictionary):
        self.__dictionary__ = dictionary
        return True

    def copy(self):
        return copy.copy(self)

    @staticmethod
    def fromkeys(keys, value):
        dictionary = {key: value for key in keys}
        return ThunkDict(dictionary)

    def keys(self):
        return list(self.__dictionary__.keys())

    def __thunk__(self, item):
        if callable(item):
            return self.__lazy__wrapper__(item)
        return item

    def __dethunk__(self, item):
        if isinstance(item, self.__LazyInternal__):
            return item.release()
        return item

    def items(self):
        return [(key, self.__dethunk__(value)) for key, value in self.__dictionary__.items()]

    def values(self):
        return [self.__dethunk__(value) for value in self.__dictionary__.values()]

    def clear(self):
        self.__dictionary__ = {}
        return True

    def __getitem__(self, key):
        obj = self.__dictionary__[key]
        self.__dictionary__[key] = self.__dethunk__(obj)
        return self.__dictionary__[key]

    def __setitem__(self, attr, item):
        self.__dictionary__[attr] = self.__thunk__(item)
        return True

    def __delitem__(self, key):
        del self.__dictionary__[key]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.__dictionary__)
