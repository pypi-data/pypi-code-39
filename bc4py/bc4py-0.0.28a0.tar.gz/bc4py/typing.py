from bc4py_extension import PyAddress
from typing import Tuple


TxInput = Tuple[bytes, int]
TxOutput = Tuple[PyAddress, int, int]


__all__ = [
    "TxInput",
    "TxOutput",
]
