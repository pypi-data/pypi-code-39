from winterboot.WinterBoot import addProvider
from winterboot.Autowired import Autowired

class Service(object):

    def __init__(self, klass):
        className = klass.__name__
        serviceId = className[0].lower() + className[1:]
        addProvider(serviceId, self)
        self.wrapped = klass
        self.singleton = None
        self.isSingleton = True

    def __call__(self):
        instance = self.getInstance()
        return instance


    def makeSureWeHaveSingleton(self):
        if self.singleton == None:
            self.singleton = self.wrapped()

    def getInstance(self, singleton=None):
        if singleton == Autowired.LAST_INSTANCE:
            return self.lastreturned
        if singleton or (self.isSingleton and singleton is None):
            self.makeSureWeHaveSingleton()
            self.lastreturned = self.singleton
            return self.lastreturned
        else:
            self.lastreturned = self.wrapped()
            return self.lastreturned

