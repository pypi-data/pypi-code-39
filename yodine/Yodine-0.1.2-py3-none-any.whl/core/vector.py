import math
import struct

from .trig import fast_sin, fast_cos



class Vector(object):
    def __init__(self, vec):
        if isinstance(vec, (list, tuple)):
            self.x = float(vec[0])
            self.y = float(vec[1])

        elif hasattr(vec, 'x') and hasattr(vec, 'y'):
            self.x = float(vec.x)
            self.y = float(vec.y)

        else:
            raise ValueError("Non-vectorial value: {}".format(repr(vec)))

    def rotate(self, angle: float) -> 'Vector':
        return Vector((
            self.x * fast_sin(angle) - self.y * fast_cos(angle),
            self.x * fast_cos(angle) + self.y * fast_sin(angle),
        ))

    def size(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def sqsize(self) -> float:
        return float(self.x ** 2 + self.y ** 2)

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
        return Vector((self.x + b.x, self.y + b.y))

    def __neg__(self) -> 'Vector':
        return Vector((-self.x, -self.y))

    def __mul__(self, b) -> 'Vector':
        if isinstance(b, type(self)):
            bv = Vector(b)
            return Vector((self.x * bv.x, self.y * bv.y))

        else:
            return Vector((self.x * b, self.y * b))

    def __truediv__(self, b) -> 'Vector':
        if isinstance(b, type(self)):
            bv = Vector(b)
            return Vector((self.x / bv.x, self.y / bv.y))

        else:
            return Vector((self.x / b, self.y / b))

    def dot(self, b: 'Vector') -> float:
        assert isinstance(b, type(self))
        return self.x * b.x + self.y * b.y

    def __sub__(self, b: 'Vector') -> 'Vector':
        return self + (-b)

    def __repr__(self) -> str:
        return "{}(x={},y={})".format(type(self).__name__, self.x, self.y)


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

    def __getattr__(self, name: str):
        if name in 'xy':
            return self.component.value[0 if name == 'x' else 1]

    def __setattr__(self, name: str, value: any):
        if name in 'xy':
            val = [self.x, self.y]

            if name == 'x':
                val[0] = float(value)

            elif name == 'y':
                val[1] = float(value)

            self.component.set(val)

        else:
            super().__setattr__(name, value)