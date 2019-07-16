import hashlib
import hmac


def sha256(s: bytes)->bytes:
    h = hashlib.sha256()
    h.update(s)
    return h.digest()


def sha256loop(s: bytes, cnt: int)->bytes:
    for _ in range(cnt):
        s = sha256(s)
    return s


def ripemd160(s: bytes)->bytes:
    h = hashlib.new('ripemd160')
    h.update(s)
    return h.digest()


def hmacsha256(key: bytes, s: bytes)->bytes:
    h = hmac.new(key, s, 'sha256')
    return h.digest()
