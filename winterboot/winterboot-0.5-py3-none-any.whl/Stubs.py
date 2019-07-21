from winterboot import WinterBoot

class Stubs(object):
    def __init__(self, klass_or_name):
        if str == type(klass_or_name):
            self.name = klass_or_name
        else:
            self.name = None
            self.__call__(klass_or_name)

    def __call__(self,klass):
        self.klass = klass
        if self.name is None:
            self.name = klass.__name__
        if not self.name in WinterBoot.stubs:
            WinterBoot.stubs[self.name] = []
        WinterBoot.stubs[self.name] = self
        return self
