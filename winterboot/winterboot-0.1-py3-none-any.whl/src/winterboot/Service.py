from winterboot.WinterBoot import addProvider

class Service(object):

    def __init__(self, klass):
        className = klass.__name__
        serviceId = className[0].lower() + className[1:]
        instance = self.instantiateIfType(klass)
        addProvider(serviceId, instance)
        self.wrapped = instance

    def __call__(self):
        return self.wrapped

    def instantiateIfType(self, provider):
        if type(provider) == type:
            provider = provider()
        return provider


