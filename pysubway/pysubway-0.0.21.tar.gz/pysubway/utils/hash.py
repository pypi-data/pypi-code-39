import base64
import hashlib
import hmac
from typing import Union

try:
    from utils.ustring import to_bytes, to_str
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils.ustring import to_bytes, to_str

def hash_hmac(key: Union[str, bytes], msg: Union[str, bytes], digestmod=hashlib.sha1,
              returned_value_type: Union[str, bytes] = str, need_base64_encode=False) -> Union[
    str, bytes]:
    obj = hmac.new(to_bytes(key), to_bytes(msg), digestmod=digestmod)
    if need_base64_encode:
        return to_str(base64.b64encode(obj.digest()))
    if returned_value_type == str:
        return obj.hexdigest()
    elif returned_value_type in (bytes, bytearray):
        return obj.digest()
    else:
        raise NotImplementedError(f'returned_value_type {returned_value_type} is not supported')


def hash_md5(plaintext: str) -> str:
    m = hashlib.md5()
    m.update(to_bytes(plaintext))
    return m.hexdigest()
