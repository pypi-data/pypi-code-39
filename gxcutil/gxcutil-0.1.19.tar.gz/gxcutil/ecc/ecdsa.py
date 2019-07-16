from .secp256k1 import Secp256k1

from ..utils import mod_inv, from_bytes
from .curve import Curve
from .point import ECCPoint

from typing import Tuple
import secrets

_wnaf_cache = [None, Secp256k1.G, Secp256k1.G.double()]

_key_byte1 = 0xff00000000000000000000000000000000000000000000000000000000000000  # 32 bytes
_key_byte2 = 0x00ff000000000000000000000000000000000000000000000000000000000000  # 32 bytes
_canonical_byte1 = 0x8000000000000000000000000000000000000000000000000000000000000000  # 32 bytes
_canonical_byte2 = 0x0080000000000000000000000000000000000000000000000000000000000000  # 32 bytes


for _ in range(3, 1 << 8):
    _wnaf_cache.append(_wnaf_cache[-1] + _wnaf_cache[1])


def _is_canonical(r: int, s: int)->bool:
    return (
            not (_canonical_byte1 & r)
            and not (_key_byte1 & r == 0 and not (_canonical_byte2 & r))
            and not (_canonical_byte1 & s)
            and not (_key_byte1 & s == 0 and not (_canonical_byte2 & s))
    )


def _get_recovery_param(hash_data: int, r: int, s: int, pub_x: int, pub_y: int, curve: Curve = None, cache=None)-> int or None:
    if curve is None:
        cache = _wnaf_cache
        curve = Secp256k1

    R = ECCPoint(r, None, curve)
    # nR = R.multiply(curve.n)
    # if nR is not None:
    #     raise RuntimeError('nR is not INF')

    # data_neg = (-data) % curve.n
    data_neg = curve.n - hash_data
    data_neg_G = curve.G.multiply(data_neg, cache)
    r_inv = mod_inv(r, curve.n)

    Q = R.multiply(s) + data_neg_G
    Q = Q.multiply(r_inv)

    if Q.x == pub_x and Q.y == pub_y:
        return R.y & 1

    # R = -R
    # Q = R.multiply(s) + data_neg_G
    # Q = Q.multiply(r_inv)
    #
    # if Q.x == pub_x and Q.y == pub_y:
    #     return R.y & 1
    return 1 - (R.y & 1)

    # return None


def sign(key: int, hash_data: int, pub: Tuple[int, int] = None, curve: Curve = None, cache=None)->Tuple[int, int, int]:
    if curve is None:
        cache = _wnaf_cache
        curve = Secp256k1

    n_bytes = (curve.n.bit_length() + 7) // 8
    n_div2 = curve.n >> 1

    hash_data %= curve.n

    if pub is None:
        pub_x, pub_y = key_to_pub(key, curve, cache)
    else:
        pub_x, pub_y = pub

    while True:
        k = from_bytes(secrets.token_bytes(n_bytes)) % (curve.n - 2) + 1
        kG = curve.G.multiply(k, cache)

        if kG is None:
            continue

        r = kG.x % curve.n
        s = (mod_inv(k, curve.n) * (hash_data + key * r)) % curve.n

        if s > n_div2:
            s = curve.n - s

        if not _is_canonical(r, s):
            continue

        i = _get_recovery_param(hash_data, r, s, pub_x, pub_y, curve, cache)
        if i is None:
            raise RuntimeError('Cannot find recovery param')
        break

    i += 31
    return i, r, s


def verify(pub: Tuple[int, int], hash_data: int, r: int, s: int, curve: Curve = None, cache=None)->bool:
    if curve is None:
        cache = _wnaf_cache
        curve = Secp256k1

    if not (0 < r < curve.n and 0 < s < curve.n):
        return False

    Q = ECCPoint(pub[0], pub[1], curve)

    c = mod_inv(s, curve.n)

    u1 = (hash_data * c) % curve.n
    u2 = (r * c) % curve.n

    u1G = curve.G.multiply(u1, cache)
    u2Q = Q.multiply(u2)

    if u1G is None or u2Q is None:
        return False

    R = u1G + u2Q

    if R is None:
        return False

    v = R.x

    return v == r


def pub_x_to_pub_y(pub_x: int, is_odd: bool, curve: Curve = None)->int:
    if curve is None:
        curve = Secp256k1

    Q = ECCPoint(pub_x, None, curve)
    pub_y = Q.y
    if (pub_y % 2) ^ is_odd:
        pub_y = (-pub_y) % curve.p

    return pub_y


def key_to_pub(key: int, curve: Curve = None, cache=None)->Tuple[int, int]:
    if curve is None:
        cache = _wnaf_cache
        curve = Secp256k1

    keyG = curve.G.multiply(key, cache)

    return keyG.x, keyG.y


def random_key(curve: Curve = None)->int:
    if curve is None:
        curve = Secp256k1

    return secrets.randbelow(curve.n)
