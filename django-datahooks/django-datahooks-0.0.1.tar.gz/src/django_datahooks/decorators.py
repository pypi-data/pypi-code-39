from .registry import register_provider


def register(cls=None):
    if cls:
        register_provider(cls)
        return cls
    else:
        def _wrapped(cls):
            register_provider(cls)
            return cls
    return _wrapped
