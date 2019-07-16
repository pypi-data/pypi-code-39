import hashlib
import random
import time
from uuid import uuid4

LOWERCASE_ALPHA = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE_ALPHA = LOWERCASE_ALPHA.upper()
ALPHA = LOWERCASE_ALPHA + UPPERCASE_ALPHA
DIGITS = "0123456789"
ALPHA_NUM = ALPHA + DIGITS


def gen_token(gen, length):
    res = ""
    while len(res) < length:
        rem = length - len(res)
        res += gen()[:rem]
    return res


def hex_token(length=8):
    def gen():
        return hashlib.sha256((str(uuid4()) + str(time.time())).encode()).hexdigest()
    return gen_token(gen, length)


def token(sigma=ALPHA_NUM, length=8):
    def gen():
        return sigma[random.randint(0, len(sigma)-1)]
    return gen_token(gen, length)


def alpha_token(length=8):
    return token(ALPHA, length)


def digits_token(length=8):
    return token(DIGITS, length)


def alphanum_token(length=8):
    return token(ALPHA_NUM, length)


def number_token(lo, hi, length=None):
    res = str(random.randint(lo, hi))
    if length and len(res) < length:
        res = '0' * (length - len(res)) + res
    return res


def uuid_token(length=36):
    def gen():
        return str(uuid4())
    return gen_token(gen, length)
