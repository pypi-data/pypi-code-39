from winterboot.WinterBoot import addConsumer, wireOneService


class Autowired(object):
    LAST_INSTANCE = "last instance"

    def __init__(self, moduleName, decorate = None, singleton=None):
        self.singleton = singleton
        addConsumer(moduleName, self)
        self.moduleName = moduleName
        wireOneService(moduleName,lazy=True)
        self.decorate = decorate

    def __call__(self):
        return self.provider.getInstance(self.singleton)

    def __enter__(self ):
        instance = self.provider.getInstance(self.singleton)
        if self.decorate:
            setattr(self.decorate, self.moduleName, instance)
        return instance

    def __exit__(self, exceptionType, value, traceback):
        pass