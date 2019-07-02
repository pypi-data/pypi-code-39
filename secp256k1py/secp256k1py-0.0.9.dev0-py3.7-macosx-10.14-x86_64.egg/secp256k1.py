# coding=utf8

import base64
import hashlib
import random
from os import urandom
from sys import version_info
import secp256k1py.functions
from salsa20 import Salsa20_xor


class PrivateKey():
    def __init__(self, _d):
        self.d = _d

    @classmethod
    def restore(cls, hex_str):
        if version_info.major != 2:
            return cls(int(hex_str, 16))
        else:
            return cls(long(hex_str, 16))

    def __repr__(self):
        if version_info.major != 2:
            return hex(self.d)[2:]
        else:
            return hex(self.d)[2:-1]

    def generate_secret(self, publickey):
        """
        生成共享秘密
        :param publickey:
        :return:
        """
        point = secp256k1py.functions.scalar_mult(self.d, publickey.Q)
        x, y = point
        if version_info.major != 2:
            return "%s%s" % (hex(x)[2:], hex(y)[2:])
        else:
            return "%s%s" % (hex(x)[2:-1], hex(y)[2:-1])


    def sign(self, message):
        """
        签名消息
        :param message:
        :return:
        """
        point = secp256k1py.functions.sign_message(self.d, message)
        x, y = point
        if version_info.major != 2:
            return "%s%s" % (hex(x)[2:], hex(y)[2:])
        else:
            return "%s%s" % (hex(x)[2:-1], hex(y)[2:-1])

    def decrypt(self, publicKey, b64encrypted, b64iv):
        """
        解压数据
        :param publicKey:
        :param b64encrypted:
        :param b64iv:
        :return:
        """
        if version_info.major != 2:
            secret = self.generate_secret(publicKey)
            print(type(secret), secret)
            uncompress_key = bytes.fromhex(secret)
        else:
            uncompress_key = self.generate_secret(publicKey).decode('hex')
        key = hashlib.sha256(uncompress_key).digest()
        print('key:%s' % key)
        raw_enc_bytes = base64.urlsafe_b64decode(b64encrypted)
        iv = base64.urlsafe_b64decode(b64iv)
        if version_info.major != 2:
            raw_bytes = Salsa20_xor(raw_enc_bytes, iv, key)
            return raw_bytes.decode('utf8')
        else:
            return Salsa20_xor(raw_enc_bytes, iv, key)


class PublicKey():
    def __init__(self, _q):
        self.Q = _q

    @classmethod
    def restore(cls, hex_str):
        if version_info.major != 2:
            point = (
                int(hex_str[:64], 16),
                int(hex_str[64:], 16)
            )
        else:
            point = (
                long(hex_str[:64], 16),
                long(hex_str[64:], 16)
            )
        return cls(point)

    def verify(self, message, signature):
        """
        对消息验签
        :param message:
        :param signature:
        :return:
        """
        if version_info.major != 2:
            point = (
                int(signature[:64], 16),
                int(signature[64:], 16)
            )
        else:
            point = (
                long(signature[:64], 16),
                long(signature[64:], 16)
            )
        return secp256k1py.functions.verify_signature(self.Q, message, point)

    def encrypt(self, privateKey, message):
        """
        用共享秘密加密数据
        :param privateKey:
        :return:
        """
        if version_info.major != 2:
            secret = privateKey.generate_secret(self)
            print(type(secret), secret)
            uncompress_key = bytes.fromhex(secret)
            message = message.encode('utf8')
        else:
            uncompress_key = privateKey.generate_secret(self).decode('hex')
        key = hashlib.sha256(uncompress_key).digest()
        print('key:%s' % key)
        iv = urandom(8)
        enc = Salsa20_xor(message, iv, key)
        b64_enc = base64.urlsafe_b64encode(enc)
        b64_iv = base64.urlsafe_b64encode(iv)
        return dict(
            enc=b64_enc,
            iv=b64_iv
        )

    def __repr__(self):
        x, y = self.Q
        if version_info.major != 2:
            return "%s%s" % (hex(x)[2:], hex(y)[2:])
        else:
            return "%s%s" % (hex(x)[2:-1], hex(y)[2:-1])


class KeyPair():
    def __init__(self, private, public):
        self.privateKey = private
        self.publicKey = public


def make_keypair():
    """Generates a random private-public key pair."""
    private_key = random.randrange(1, secp256k1py.functions.curve.n)
    public_key = secp256k1py.functions.scalar_mult(private_key, secp256k1py.functions.curve.g)
    return KeyPair(PrivateKey(private_key), PublicKey(public_key))
