from Crypto.Cipher import AES
from Crypto import Random

import base64
import hashlib


def _pad(s: str, size: int)->str:
    p = size - len(s) % size
    return s + p * chr(p)


def _unpad(s: str)->str:
    return s[:-ord(s[-1])]


def encrypt(key: str, original_text: str)->str:
    raw = _pad(original_text, AES.block_size)
    iv = Random.new().read(AES.block_size)
    digested_key = hashlib.sha256(key.encode('utf-8')).digest()
    cipher = AES.new(digested_key, AES.MODE_CBC, iv)

    return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')


def decrypt(key: str, encrypted_text: str)-> str or None:
    enc = base64.b64decode(encrypted_text)
    iv = enc[:AES.block_size]
    digested_key = hashlib.sha256(key.encode('utf-8')).digest()
    cipher = AES.new(digested_key, AES.MODE_CBC, iv)

    try:
        gxc_private_key = _unpad(cipher.decrypt(enc[AES.block_size:]).decode('utf-8'))
    except:
        return None
    return gxc_private_key
