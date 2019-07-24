providers = {}


def register_provider(cls):
    providers[cls.name] = cls
