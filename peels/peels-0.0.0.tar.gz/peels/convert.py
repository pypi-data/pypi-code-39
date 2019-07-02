from enum import IntFlag
from struct import pack
import sys
from typing import Any, Union
import inspect


ENDIAN = "big"


class Converter:

    ID: str = None

    @staticmethod
    def load(data: bytes):
        raise NotImplemented

    @staticmethod
    def dump(data: Any, length: int):
        raise NotImplemented


class NoConverter(Converter):
    ID = "-"

    @staticmethod
    def load(data: bytes):
        return data

    @staticmethod
    def dump(data: Union[bytes, int], _):
        return data


class UIntegerConverter(Converter):
    ID = "I"

    @staticmethod
    def load(data: bytes):
        return int.from_bytes(data, ENDIAN, signed=False)

    @staticmethod
    def dump(data: int, length: int):
        return data.to_bytes(length, ENDIAN, signed=False)


class SIntegerConverter(Converter):
    ID = "i"

    @staticmethod
    def load(data: bytes):
        return int.from_bytes(data, ENDIAN, signed=True)

    @staticmethod
    def dump(data: int, length: int):
        return data.to_bytes(length, ENDIAN, signed=True)


class ByteConverter(Converter):
    ID = "Y"

    @staticmethod
    def load(data: bytes):
        return data

    @staticmethod
    def dump(data: bytes, length: int):
        if len(data) > length:
            raise ValueError("Data is too large to fit inside length")
        return pack(str(length) + "s", data)


class UnicodeConverter(Converter):
    ID = "U"

    @staticmethod
    def load(data: bytes):
        return data.decode("utf-8")

    @staticmethod
    def dump(data: str, length: int):
        data = data.encode("utf-8")
        if len(data) > length:
            raise ValueError("Data is too large to fit inside length")
        return pack(str(length) + "s", data)


class BoolConverter(Converter):
    ID = "B"

    @staticmethod
    def load(data: int):
        return bool(data)

    @staticmethod
    def dump(data: bool, _):
        return int(data)


class FlagConverter(Converter, IntFlag):

    @classmethod
    def load(cls, data: Union[bytes, int]):
        data = data if isinstance(data, int) else UIntegerConverter.load(data)
        return cls(data)

    @staticmethod
    def dump(value: IntFlag, length: int):
        return value.value


clsmembers = [c[1] for c in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
convert_map = {c.ID: c for c in clsmembers if issubclass(c, Converter) and getattr(c, "ID", None)}
