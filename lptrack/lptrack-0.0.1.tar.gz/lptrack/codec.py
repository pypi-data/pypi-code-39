"""Provides the reader and writer for converting between Python primitives and
their byte representation."""

import io
import struct
from typing import BinaryIO, Optional

__all__ = ["Reader", "Writer"]

_FORMAT_BOOL = "?"
_FORMAT_BYTE = "b"
_FORMAT_INT = ">i"
_FORMAT_LONG = ">q"
_FORMAT_USHORT = ">H"


class Reader:
    _stream: BinaryIO

    def __init__(self, stream: BinaryIO) -> None:
        self._stream = stream

    @property
    def stream(self) -> BinaryIO:
        return self._stream

    def read_bool(self) -> bool:
        return struct.unpack(_FORMAT_BOOL, self._stream.read(1))[0]

    def read_byte(self) -> int:
        return struct.unpack(_FORMAT_BYTE, self._stream.read(1))[0]

    def read_int(self) -> int:
        return struct.unpack(_FORMAT_INT, self._stream.read(4))[0]

    def read_long(self) -> int:
        return struct.unpack(_FORMAT_LONG, self._stream.read(8))[0]

    def read_ushort(self) -> int:
        return struct.unpack(_FORMAT_USHORT, self._stream.read(2))[0]

    def read_utf(self) -> str:
        return self._stream.read(self.read_ushort()).decode("utf-8")

    def read_optional_utf(self) -> Optional[str]:
        if self.read_bool():
            return self.read_utf()
        else:
            return None


class Writer:
    _stream: BinaryIO

    def __init__(self, stream: BinaryIO = None) -> None:
        if stream is None:
            stream = io.BytesIO()

        self._stream = stream

    @property
    def stream(self) -> BinaryIO:
        return self._stream

    def write_bool(self, data: bool) -> None:
        self._stream.write(struct.pack(_FORMAT_BOOL, data))

    def write_byte(self, data: int) -> None:
        self._stream.write(struct.pack(_FORMAT_BYTE, data))

    def write_int(self, data: int) -> None:
        self._stream.write(struct.pack(_FORMAT_INT, data))

    def write_long(self, data: int) -> None:
        self._stream.write(struct.pack(_FORMAT_LONG, data))

    def write_ushort(self, data: int) -> None:
        self._stream.write(struct.pack(_FORMAT_USHORT, data))

    def write_utf(self, data: str) -> None:
        data = data.encode("utf-8")
        self.write_ushort(len(data))
        self._stream.write(data)

    def write_optional_utf(self, data: Optional[str]) -> None:
        if data is None:
            self.write_bool(False)
        else:
            self.write_bool(True)
            self.write_utf(data)
