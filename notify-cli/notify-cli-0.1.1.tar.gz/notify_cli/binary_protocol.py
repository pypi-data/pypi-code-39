import struct
from contextlib import suppress


def bytes_to_u32(x):
    return struct.unpack('<L', x)[0]


def u32_to_bytes(x) -> bytes:
    return bytes(struct.pack('<L', x))


class BinaryProtocol:
    """A client for simple length-prefixed socket communication"""

    def __init__(self, socket):
        self.socket = socket

    def send(self, msg: bytes):
        if isinstance(msg, str):
            msg = msg.encode()
        len_bytes = u32_to_bytes(len(msg))
        bs = len_bytes + msg
        self.socket.sendall(bs)

    def receive(self) -> bytes:
        length = bytes_to_u32(self._read_bytes(4))
        return self._read_bytes(length)

    def close(self):
        with suppress(OSError):
            self.socket.shutdown(2)
        self.socket.close()

    def _read_bytes(self, n: int) -> bytes:
        buf = b''
        while len(buf) < n:
            new_data = self.socket.recv(n - len(buf))
            if not new_data:
                self.close()
                raise ConnectionAbortedError
            buf += new_data
        return buf
