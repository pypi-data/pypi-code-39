import logging
log = logging.getLogger()

class dotdict(dict):
    """ dot.notation access to dictionary attributes """
    __getattr__= dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    # this is required for pickle to work
    def __getstate__(self):
        return vars(self)
    def __setstate__(self, d):
        pass