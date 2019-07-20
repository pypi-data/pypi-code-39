from unittest.mock import MagicMock
from winterboot import WinterBoot

class MockedService:
    def __init__(self, moduleName, instanceToDecorate=None):
        self.moduleName = moduleName
        self.provider = MagicMock()
        if instanceToDecorate:
            setattr(instanceToDecorate, moduleName, self.provider)

    def __enter__(self):
        self.orig = WinterBoot.providers[self.moduleName][0]
        WinterBoot.providers[self.moduleName][0]=self
        WinterBoot.wireOneService(self.moduleName)
        return self.provider

    def __exit__(self, exceptionType, value, traceback):
        WinterBoot.providers[self.moduleName][0] = self.orig
        WinterBoot.wireOneService(self.moduleName)

    def getInstance(self, singleton=True):
        return self.provider