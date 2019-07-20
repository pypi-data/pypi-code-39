from winterboot.WinterBoot import addConsumer, wireOneService

class Autowired(object):

    def __init__(self, moduleName):
        addConsumer(moduleName, self)
        self.moduleName = moduleName
        wireOneService(moduleName,lazy=True)
        
    def __getattribute__(self, name):
        if name in ['provider', '__getattribute__', '__dict__', 'moduleName']:
            return object.__getattribute__(self,name)
        if not 'provider' in self.__dict__.keys():
            raise AttributeError('No service registered with name {0}'.format(self.moduleName))
        return getattr(self.provider, name)
