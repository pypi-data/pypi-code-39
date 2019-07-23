"""

typevalidation/decorator.py

written by: Oliver Cordes 2019-07-01
changed by: Oliver Cordes 2019-07-20

"""

from functools import wraps

from typevalidation.types import *


class typevalidate(object):
    def __init__ (self, *args, **kwargs):
        # store arguments passed to the decorator
        self.args = args
        self.kwargs = kwargs

        for key, val in kwargs.items():
            if key == 'isclass':
                self._isclass = val


    def __call__(self, func):
        msg = func.__qualname__
        a   = dir(func)

        @wraps(func)
        def wrap(*args, **kwargs):
            #print(msg)
            #print(func.__annotations__)
            args, kwargs = self.convert(args, kwargs, func.__annotations__)
            return func(*args, **kwargs)

        return wrap


    def convert(self, args, kwargs, newtypes):
        newtypesargs = [ val for key,val in newtypes.items()]

        # converting args, iterating over indices...
        if self._isclass:
            indx = 1
        else:
            indx = 0

        # sanity checks
        # not perfect, since we cannot handle the case that there is a
        # annotation missing and if there are more parameters given in the
        # call than defined ...
        if len(newtypesargs) < (len(args)+len(kwargs)-indx):
            print('WARNING: Number of annotations doesn\'t match the number of arguments!')
            return args, kwargs

        #print(newtypesargs)

        tindx = 0
        args = list(args)
        while indx < len(args):
            #print(indx, type(args[indx]))
            newval = self.converttype(args[indx], newtypesargs[tindx])
            args[indx] = newval
            indx += 1
            tindx += 1
        return args, kwargs


    def converttype(self, val, newtype):
        # do the real type conversion
        if newtype is None:
            return val
        else:
            return newtype(val)
        #if newtype in basic_types:
        #    return newtype(val)
        #else:
        #    return newtype(val)
