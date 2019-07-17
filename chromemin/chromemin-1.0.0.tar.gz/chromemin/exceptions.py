
__all__ = [
    'ChromeException',
    'TimeoutError',
    'ProtocolError'
]

class ChromeException(Exception):
    pass

class TimeoutError(Exception):
    pass

class ProtocolError(ChromeException):
    pass