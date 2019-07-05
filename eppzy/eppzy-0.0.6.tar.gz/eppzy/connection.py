import socket
import ssl
from contextlib import contextmanager
from struct import pack, unpack
from logging import getLogger


_log = getLogger(__name__)


class LengthPrefixed:
    def __init__(self, s):
        self._s = s

    def send(self, b):
        _log.debug("sending: %r", b)
        b = pack("!i", len(b)) + b
        self._s.send(b)

    def recv(self):
        _log.debug("receiving")
        r = self._s.recv(4)
        l, = unpack("!i", r)
        _log.debug("expecting %s bytes", l)
        v = self._s.recv(l)
        _log.debug("recieved %r", v)
        return v


def connect(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    ss = ssl.wrap_socket(s)
    _log.info('connecting to %s:%s', host, port)
    ss.connect((host, port))
    _log.debug('connected to %s:%s', host, port)
    return ss


@contextmanager
def connection(host, port):
    ss = connect(host, port)
    try:
        yield ss
    finally:
        _log.debug('closing connection to %s:%s', host, port)
        ss.close()
