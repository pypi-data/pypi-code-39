from unittest.mock import MagicMock, patch
from winterboot import WinterBoot

class MockedService:
    def __init__(self, moduleName, instanceToDecorate=None):
        self.moduleName = moduleName
        self.provider = MagicMock()
        if instanceToDecorate:
            setattr(instanceToDecorate, moduleName, self.provider)


    def __enter__(self):
        if self.moduleName in WinterBoot.providers:
            self.orig = WinterBoot.providers[self.moduleName][0]
        else:
            self.orig = None
            self.patcher = patch(self.moduleName)
            self.provider =  self.patcher.start()
            WinterBoot.providers[self.moduleName] = [None]
        WinterBoot.providers[self.moduleName][0]=self
        WinterBoot.wireOneService(self.moduleName)
        if self.moduleName.endswith("Service"):
            stubName = self.moduleName[:-7]+'Stubs'
            stubName = stubName[0].upper() + stubName[1:]
        else:
            stubName = self.moduleName
        if stubName in WinterBoot.stubs:
            stubInstance = WinterBoot.stubs[stubName].klass()
            stubInstance.behaviour(self.provider)
        return self.provider

    def __exit__(self, exceptionType, value, traceback):
        WinterBoot.providers[self.moduleName][0] = self.orig
        WinterBoot.wireOneService(self.moduleName)
        if hasattr(self, 'patcher'):
            self.patcher.stop()
            del(WinterBoot.providers[self.moduleName])

    def getInstance(self, singleton=True):
        return self.provider
    WinterBoot.stubs
