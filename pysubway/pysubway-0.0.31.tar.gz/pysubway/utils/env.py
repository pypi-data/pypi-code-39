import os

import sys

IS_PY3 = sys.version_info.major == 3


def getenv(key: str, default: str, ignore_upper: bool = True) -> str:
    _key = key.lower() if ignore_upper else key
    value = os.getenv(_key) or default
    print("\033[033m", f'{_key} ---------------------> {value}', "\033[0m")
    return value
