# -*- coding: utf-8 -*-

from functools import update_wrapper, partial


class Hook:
    def __init__(self, func):
        update_wrapper(self, func)
        self.befores = []
        self.afters = []
        self.basefunc = func

    def before(self, func):
        if callable(func):
            self.befores.append(func)
        return func

    def after(self, func):
        if callable(func):
            self.afters.append(func)
        return func

    def __get__(self, obj, objtype):
        func = partial(self.__call__, obj)
        func.before = self.before
        func.after = self.after
        return func

    def __call__(self, *args, **kwargs):
        for func in self.befores:
            func(*args, **kwargs)
        result = self.basefunc(*args, **kwargs)
        for func in self.afters:
            func(*args, **kwargs)
        return result
