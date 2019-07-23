from winterboot.Autowired import Autowired

class TestDataForStub(Autowired):
    def __init__(self, moduleName, decorate = None, singleton = Autowired.LAST_INSTANCE):
        super().__init__(moduleName, decorate, singleton)

