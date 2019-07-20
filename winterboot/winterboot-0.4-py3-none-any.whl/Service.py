from winterboot.WinterBoot import addProvider

class Service(object):

    def __init__(self, klass):
        className = klass.__name__
        serviceId = className[0].lower() + className[1:]
        addProvider(serviceId, self)
        self.wrapped = klass
        self.singleton = None

    def __call__(self):
        instance = self.getInstance()
        return instance

    def getInstance(self, singleton = True):
        if singleton:
            if self.singleton == None:
                self.singleton = self.wrapped()
            return self.singleton
        else:
            return self.wrapped()

