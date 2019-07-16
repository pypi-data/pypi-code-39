from .curve import Curve
from .point import ECCPoint

_G = ECCPoint(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
    0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    0x00,
    0x07,
)


class _Secp256k1(Curve):
    @property
    def p(self)->int:
        return 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f

    @property
    def a(self)->int:
        return 0x00

    @property
    def b(self)->int:
        return 0x07

    @property
    def n(self)->int:
        return 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

    @property
    def h(self)->int:
        return 0x01

    @property
    def G(self)->ECCPoint:
        return _G


Secp256k1 = _Secp256k1()
