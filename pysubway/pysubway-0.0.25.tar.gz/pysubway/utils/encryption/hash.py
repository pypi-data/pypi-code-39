import hashlib

try:
    from utils.ustring import to_bytes
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils.ustring import to_bytes


def md5(plaintext: str) -> str:
    md5 = hashlib.md5()
    md5.update(to_bytes(plaintext))
    s = md5.hexdigest()
    return s


if __name__ == '__main__':
    print(md5('123445'))
