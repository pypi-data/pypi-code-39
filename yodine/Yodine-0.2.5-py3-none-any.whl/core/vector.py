import math
import struct

from .trig import fast_sin, fast_cos



class Vector(object):
    def __init__(self, x, y = None):
        if y:
            self.x = x
            self.y = y

        else:
            try:
                self.x, self.y = x

            except TypeError:
                raise ValueError("Non-vectorial value: {}".format(repr(x)))

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, co):
        if co in (0, 'x'):
            return self.x

        if co in (1, 'y'):
            return self.y

        raise KeyError("No such key in a vector: ", repr(co))

    def ints(self):
        return Vector((
            int(self[0]),
            int(self[1])
        ))

    def rotate(self, angle: float) -> 'Vector':
        c = math.cos(angle)
        s = math.sin(angle)

        return Vector((
            self.x * c - self.y * s,
            self.x * s + self.y * c,
        ))

    def size(self) -> float:
        return math.sqrt(self[0] ** 2 + self[1] ** 2)

    def sqsize(self) -> float:
        return float(self[0] ** 2 + self[1] ** 2)

    def fisrsize(self) -> float:
        y = self.sqsize()
        threehalfs = 1.5
        x2 = y * 0.5
    
        packed_y = struct.pack('f', y)       
        i = struct.unpack('i', packed_y)[0]  # treat float's bytes as int 
        i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
        packed_i = struct.pack('i', i)
        y = struct.unpack('f', packed_i)[0]  # treat int's bytes as float
        
        y = y * (threehalfs - (x2 * y * y))  # Newton's method
        return y

    def unit(self) -> 'Vector':
        if self.sqsize() == 0:
            return Vector((0, 0))

        if self.sqsize() == 1:
            return self

        return self * self.fisrsize()

    def __add__(self, b: 'Vector') -> 'Vector':
        return Vector((self[0] + b.x, self[1] + b.y))

    def __neg__(self) -> 'Vector':
        return Vector((-self[0], -self[1]))

    def __mul__(self, b) -> 'Vector':
        try:
            return Vector((self[0] * b.x, self[1] * b.y))

        except AttributeError:
            return Vector((self[0] * b, self[1] * b))

    def __truediv__(self, b) -> 'Vector':
        try:
            return Vector((self[0] / b.x, self[1] / b.y))

        except AttributeError:
            return Vector((self[0] / b, self[1] / b))

    def dot(self, b: 'Vector') -> float:
        return self[0] * b.vec[0] + self[1] * b.vec[1]

    def __sub__(self, b: 'Vector') -> 'Vector':
        return self + (-b)

    def __repr__(self) -> str:
        return "{}(x={},y={})".format(type(self).__name__, self[0], self[1])


class ComponentVector(Vector):
    def __init__(self, component: 'Component'):
        self.component = component

    def __iadd__(self, b: 'Vector') -> 'ComponentVector':
        res = self + b
        self.x = res.x
        self.y = res.y
        return self

    def __isub__(self, b: 'Vector') -> 'ComponentVector':
        res = self - b
        self.x = res.x
        self.y = res.y
        return self

    def __imul__(self, b: 'Vector') -> 'ComponentVector':
        res = self * b
        self.x = res.x
        self.y = res.y
        return self

    def __itruediv__(self, b: 'Vector') -> 'ComponentVector':
        res = self / b
        self.x = res.x
        self.y = res.y
        return self

    def __lshift__(self, b: 'Vector') -> 'ComponentVector':
        self.x = b.x
        self.y = b.y
        return self

    @property
    def x(self):
        return self.component.value[0]

    @property
    def y(self):
        return self.component.value[1]

    @x.setter
    def x(self, val):
        self.component.value = [val, self.component.value[1]]

    @y.setter
    def y(self, val):
        self.component.value = [self.component.value[0], val]