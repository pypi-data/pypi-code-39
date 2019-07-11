def BitMask(num_bits):
    """ Returns num_bits 1s in binary """
    return (1<<num_bits) - 1

def BitNot(n, num_bits):
    return BitMask(num_bits) - n

class FixedInt(object):
    def __init__(self, value, num_bits=32):
        self.num_bits = num_bits
        self.value = value & BitMask(num_bits)

    def __str__(self):
        return str(self.num_bits) + "bits: " + str(self.value)

    def __add__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value + other.value, self.num_bits)
        
    def __sub__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value - other.value, self.num_bits)
    
    def __mul__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value * other.value, self.num_bits)
    
    def __truediv__(self, other):
        return self//other
    
    def __floordiv__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value//other.value, self.num_bits)
        
    def __mod__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value%other.value, self.num_bits)
    
    def __pow__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value**other.value, self.num_bits)

    def __and__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value & other.value, self.num_bits)

    def __or__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value | other.value, self.num_bits)

    def __xor__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value ^ other.value, self.num_bits)
    
    def __lshift__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value << other.value, self.num_bits)

    def __rshift__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return FixedInt(self.value >> other.value, self.num_bits)

    def __iadd__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value += other.value
        self.value &= BitMask(self.num_bits)
        return self

    def __isub__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value -= other.value
        self.value &= BitMask(self.num_bits)
        return self
        
    def __imul__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value *= other.value
        self.value &= BitMask(self.num_bits)
        return self
        
    def __idiv__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value //= other.value
        self.value &= BitMask(self.num_bits)
        return self

    def __ifloordiv__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value //= other.value
        self.value &= BitMask(self.num_bits)
        return self

    def __imod__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value %= other.value
        self.value &= BitMask(self.num_bits)
        return self
        
    def __ipow__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value **= other.value
        self.value &= BitMask(self.num_bits)
        return self
        
    def __ilshift__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value <<= other.value
        self.value &= BitMask(self.num_bits)
        return self
        
    def __irshift__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value >>= other.value
        self.value &= BitMask(self.num_bits)
        return self
        
    def __iand__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value &= other.value
        self.value &= BitMask(self.num_bits)
        return self
        
    def __ior__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value |= other.value
        self.value &= BitMask(self.num_bits)
        return self
        
    def __ixor__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        self.value ^= other.value
        self.value &= BitMask(self.num_bits)
        return self
                    
    def __lt__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return self.value < other.value
    
    def __gt__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return self.value > other.value
    
    def __le__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return self.value <= other.value
    
    def __ge__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return self.value >= other.value
    
    def __eq__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return self.value == other.value
    
    def __ne__(self, other):
        if other.num_bits != self.num_bits:
            raise TypeError('Got FixedInt with width of {} bits, but expected {} bits'.format(other.num_bits, self.num_bits))
        return self.value != other.value

    def __neg__(self):
        """ This is not 'pythonic', but it is correct for general binary arithmetic """
        v = BitNot(self.value, self.num_bits) + 1
        return FixedInt(v, self.num_bits)
    def __invert__(self):
        return FixedInt(BitNot(self.value, self.num_bits))
