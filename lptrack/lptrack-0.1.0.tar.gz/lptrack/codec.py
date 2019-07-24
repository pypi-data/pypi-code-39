"""Provides the reader and writer for converting between Python primitives and
their byte representation."""
import abc
import io
import struct
from typing import BinaryIO, Optional, Union

__all__ = ["HasStream",
           "Reader", "Writer",
           "MessageInput", "MessageOutput"]

_FORMAT_BOOL = "?"
_FORMAT_BYTE = "b"
_FORMAT_INT = ">i"
_FORMAT_LONG = ">q"
_FORMAT_USHORT = ">H"


class HasStream(abc.ABC):
    @property
    @abc.abstractmethod
    def stream(self) -> BinaryIO:
        ...


class Reader(HasStream):
    _stream: BinaryIO

    def __init__(self, stream: Union[BinaryIO, HasStream]) -> None:
        if isinstance(stream, HasStream):
            stream = stream.stream

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

    def __init__(self, stream: Union[BinaryIO, HasStream] = None) -> None:
        if stream is None:
            stream = io.BytesIO()
        elif isinstance(stream, HasStream):
            stream = stream.stream

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


class MessageInput(HasStream):
    _stream: Reader
    _flags: int
    _size: int

    def __init__(self, stream: Union[BinaryIO, HasStream]) -> None:
        self._stream = Reader(stream)
        self._flags = 0
        self._size = 0

    @property
    def stream(self) -> BinaryIO:
        return self._stream.stream

    @property
    def flags(self) -> int:
        return self._flags

    def next(self) -> Optional[Reader]:
        value = self._stream.read_int()
        self._flags = (value & 0xC0000000) >> 30
        self._size = value & 0x3FFFFFFF

        if not self._size:
            return None

        data = self._stream.stream.read(self._size)

        return Reader(io.BytesIO(data))


class MessageOutput(HasStream):
    _stream: Writer
    _body_stream: io.BytesIO

    def __init__(self, stream: Union[BinaryIO, HasStream]) -> None:
        self._stream = Writer(stream)
        self._body_stream = io.BytesIO()

    @property
    def stream(self) -> BinaryIO:
        return self._stream.stream

    def start(self) -> Writer:
        self._body_stream.truncate(0)
        self._body_stream.seek(0)
        return Writer(self._body_stream)

    def commit(self, flags: int = None) -> None:
        data = self._body_stream.getvalue()
        header = len(data)
        if flags:
            header |= flags << 30

        self._stream.write_int(header)
        self._stream.stream.write(data)

    def finish(self) -> None:
        self._stream.write_int(0)
