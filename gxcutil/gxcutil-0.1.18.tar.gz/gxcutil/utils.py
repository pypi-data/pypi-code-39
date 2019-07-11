def mod_inv(n: int, p: int)->int:
    return pow(n, p - 2, p)


def int_size(n: int)->int:
    return (n.bit_length() + 7) // 8


def to_bytes(n: int, size: int or None = None, byteorder: str = 'big', signed: bool = False)->bytes:
    if size is None:
        size = int_size(n)
    return n.to_bytes(size, byteorder=byteorder, signed=signed)


def from_bytes(s: bytes, byteorder: str = 'big', signed: bool = False)->int:
    return int.from_bytes(s, byteorder=byteorder, signed=signed)
