from .utils import to_bytes


_b58char = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def b58encode(s: bytes)->bytes:
    s_len = len(s)
    s = s.lstrip(b'\x00')
    lpad = s_len - len(s)

    s_int = int.from_bytes(s, byteorder='big')

    r = []
    while s_int:
        s_int, mod = divmod(s_int, 58)
        r.append(_b58char[mod:mod+1])

    return _b58char[0:1] * lpad + b''.join(reversed(r))


def b58decode(s: bytes)->bytes:
    s_len = len(s)
    s = s.lstrip(_b58char[0:1])
    lpad = s_len - len(s)

    s_int = 0
    for c in s:
        s_int = s_int * 58 + _b58char.index(c)

    return b'\x00' * lpad + to_bytes(s_int)
