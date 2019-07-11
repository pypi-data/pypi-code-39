import base64
from typing import Union

try:
    from utils.ustring import to_bytes, to_str
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils.ustring import to_bytes, to_str


class Picture:

    @staticmethod
    def to_base64(s: Union[str, bytes, bytearray], file=False) -> str:
        if file and isinstance(s, str):
            with open(s, mode='rb') as f:
                s = f.read()
        else:
            s = to_bytes(s)
        return to_str(base64.b64encode(s))
