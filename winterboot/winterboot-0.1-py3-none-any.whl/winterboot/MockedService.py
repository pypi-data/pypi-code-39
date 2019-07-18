from unittest.mock import MagicMock
from winterboot import WinterBoot

class MockedService(object):
    def __init__(self, serviceName, instance = None):
        self.serviceName = serviceName
        if instance is None:
            self.mock = MagicMock()
        self.orig = WinterBoot.providers[serviceName][0]
        WinterBoot.providers[serviceName][0]=self.mock
        WinterBoot.wireOneService(serviceName)

    def __enter__(self):
        return self.mock

    def __exit__(self, exceptionType, value, traceback):
        WinterBoot.providers[self.serviceName][0] = self.orig
        WinterBoot.wireOneService(self.serviceName)

