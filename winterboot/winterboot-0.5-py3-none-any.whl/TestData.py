from winterboot.Service import Service

class TestData(Service):
    def __init__(self, klass):
        super().__init__(klass)
        self.isSingleton = False
