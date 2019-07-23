"""Encoder and Decoder for LavaPlayer's message format specific to track bodies."""

import dataclasses
import enum
import io
from typing import BinaryIO, Optional, Union

from . import Track, codec, versions

__all__ = ["Flags", "Header", "Decoder", "Encoder"]


class Flags(enum.IntFlag):
    """Message Flags for the track data."""
    TRACK_INFO_VERSIONED = enum.auto()

    @property
    def is_versioned(self) -> bool:
        return (self & Flags.TRACK_INFO_VERSIONED) > 0


@dataclasses.dataclass()
class Header:
    """Message header info.

    Attributes:
        flags (Flags): Flags for the message body
        size (int): Size of the message body
    """
    flags: Flags
    size: int


class Decoder:
    """Decoder for track messages.

    Attributes:
        header (Optional[Header]): Header read by `read_header`.
    """
    _stream: codec.Reader

    header: Optional[Header]

    def __init__(self, stream: Union[BinaryIO, codec.Reader]) -> None:
        if not isinstance(stream, codec.Reader):
            stream = codec.Reader(stream)

        self._stream = stream

        self.header = None

    def read_header(self) -> None:
        """Read the header of the message and store is in `header`."""
        value = self._stream.read_int()
        flags = Flags((value & 0xC0000000) >> 30)
        size = value & 0x3FFFFFFF

        self.header = Header(flags, size)

    def read_body(self) -> Track:
        """Read the `Track` body from the message."""
        assert self.header is not None, "header not read"

        if self.header.flags.is_versioned:
            version = self._stream.read_byte()
        else:
            version = 1

        reader = versions.get_reader(version)
        return reader(self._stream)

    def decode(self) -> Track:
        """Decode an entire message and return the `Track`."""
        self.read_header()
        return self.read_body()


class Encoder:
    _stream: codec.Writer
    _body_buf: Optional[io.BytesIO]
    _body_stream: Optional[codec.Writer]

    def __init__(self, stream: Union[BinaryIO, codec.Writer]) -> None:
        if not isinstance(stream, codec.Writer):
            stream = codec.Writer(stream)

        self._stream = stream
        self._body_buf = None
        self._body_stream = None

    def start_message(self) -> None:
        if self._body_buf and self._body_stream:
            self._body_buf.seek(0)
        else:
            self._body_buf = io.BytesIO()
            self._body_stream = codec.Writer(self._body_buf)

    def write_header(self, header: Header) -> None:
        value = header.size | (header.flags << 30)
        self._stream.write_int(value)

    def write_body(self, track: Track) -> Flags:
        assert self._body_stream is not None, "message not started"

        version = track.version
        if version is None:
            version = versions.LATEST_VERSION

        flags = Flags(0)

        if version > 1:
            flags |= Flags.TRACK_INFO_VERSIONED
            self._body_stream.write_byte(version)

        writer = versions.get_writer(version)
        writer(self._body_stream, track)

        return flags

    def encode(self, track: Track) -> None:
        self.start_message()

        flags = self.write_body(track)

        body_data = self._body_buf.getvalue()

        self.write_header(Header(flags, len(body_data)))

        self._stream.stream.write(body_data)
