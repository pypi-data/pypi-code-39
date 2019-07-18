from logionmath2d.add.Add import Add
from logionmath2d.sub.Sub import Sub


class Math2DOperation:

    __addClass = Add()
    __subClass = Sub()

    def add(self, a, b):
        return self.__addClass.add(a, b)

    def sub(self, a, b):
        return self.__subClass.sub(a, b)

    def multy(self, a, b):
        return a * b
