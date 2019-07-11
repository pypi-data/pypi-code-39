from gxcutil.ecc import ecdsa
from . import base58
from .hash import sha256loop, ripemd160, sha256
from .utils import to_bytes, from_bytes

from typing import Tuple, Optional


def generate_private_key()->str:
    sign_key = ecdsa.random_key()
    return sign_key_to_private_key(sign_key)


def pub_to_public_key(pub: Tuple[int, int])->str:
    x, y = pub

    compressed = b'\x03' if y % 2 else b'\x02'
    pub_body = to_bytes(x)

    return 'GXC' + base58.b58encode(b''.join((
        compressed,
        pub_body,
        ripemd160(compressed + pub_body)[:4],
    ))).decode('utf8')


def sign_key_to_private_key(sign_key: int)->str:
    key_body = to_bytes(sign_key, 32)
    private_key = b'\x80' + key_body

    return base58.b58encode(private_key + sha256loop(private_key, 2)[:4]).decode('utf8')


def public_key_to_pub(gxc_public_key: str)->Optional[Tuple[int, int]]:
    public_key = base58.b58decode(gxc_public_key[3:].encode('utf8'))
    compressed, pub_body, checksum = public_key[:1], public_key[1:33], public_key[33:37]

    pub_x = from_bytes(pub_body)
    pub_y = ecdsa.pub_x_to_pub_y(pub_x, compressed == b'\x03')

    return pub_x, pub_y


def private_key_to_sign_key(gxc_private_key: str)->Optional[int]:
    gxc_private_key = gxc_private_key.encode('utf-8')
    gxc_private_key = base58.b58decode(gxc_private_key)

    return from_bytes(gxc_private_key[1:-4])


def private_key_to_public_key(gxc_private_key: str)->str:
    sign_key = from_bytes(base58.b58decode(gxc_private_key.encode('utf8'))[1:-4])
    pub = ecdsa.key_to_pub(sign_key)
    return pub_to_public_key(pub)


def is_valid_public_key(gxc_public_key: str)->bool:
    if gxc_public_key[:3] != 'GXC':
        return False

    try:
        public_key = base58.b58decode(gxc_public_key[3:].encode('utf8'))
        if len(public_key) != 37:
            return False

        compressed, pub_body, checksum = public_key[:1], public_key[1:33], public_key[33:37]
        if compressed != b'\x02' and compressed != b'\x03':
            return False
        if ripemd160(compressed + pub_body)[:4] != checksum:
            return False
    except:
        return False

    return True


def is_valid_private_key(gxc_private_key: str)->bool:
    if len(gxc_private_key) < 5:
        return False

    try:
        gxc_private_key = gxc_private_key.encode('utf-8')
        gxc_private_key = base58.b58decode(gxc_private_key)

        if gxc_private_key[0] != 128:
            return False
        if sha256loop(gxc_private_key[:-4], 2)[:4] != gxc_private_key[-4:]:
            return False
    except:
        return False

    return True


def verify_signature(pub: Tuple[int, int], data: bytes, signature: str)->bool:
    if len(signature) < 8:
        return False

    signature = base58.b58decode(signature[7:].encode('utf8'))

    if len(signature) != 69:
        return False

    sign_body, checksum = signature[:-4], signature[-4:]

    if ripemd160(sign_body + b'K1')[:4] != checksum:
        return False

    sign_data = int.from_bytes(sha256(data), byteorder='big')
    r_bytes, s_bytes = sign_body[1:33], sign_body[33:65]
    r, s = from_bytes(r_bytes), from_bytes(s_bytes)

    return ecdsa.verify(pub, sign_data, r, s)
