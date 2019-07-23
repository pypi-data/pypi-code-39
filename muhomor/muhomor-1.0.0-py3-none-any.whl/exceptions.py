from logging import getLogger
from .utils.serialization import deserializable_exception

logger = getLogger(__name__)


class RemoteError(Exception):
    pass


class FileTypeNotSupported(Exception):
    pass


class DatabaseUriNotFound(Exception):
    pass


class ConfigurationError(Exception):
    pass


class CommandError(Exception):
    pass


class ConsumingTimeout(Exception):
    pass


class NoServiceContainersFound(Exception):
    pass


class WrongServiceContainerType(Exception):
    pass


class NotEnoughWorkers(BaseException):
    pass


class RpcMethodCallTimeout(Exception):
    pass


class ConsumingConnectionError(Exception):
    pass


class BadRequest(Exception):
    pass


class RpcMethodNotFound(Exception):
    pass


class InternalError(Exception):
    pass


class PublishingError(Exception):
    pass


class UnknownService(Exception):
    def __init__(self, service_name):
        self.msg = f'Unknown service `{self.service_name}`'
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class UnserializableValueError(Exception):
    def __init__(self, value):
        try:
            self.repr_value = repr(value)
        except:
            logger.exception('Repr failed in UnserializableValueError')
            self.repr_value = '[__repr__ failed]'
        self.msg = f'Unserializable value: `{self.repr_value}`'
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


@deserializable_exception
class MethodNotFound(BadRequest):
    pass


@deserializable_exception
class IncorrectSignature(BadRequest):
    pass


@deserializable_exception
class AccessDenied(Exception):
    pass


@deserializable_exception
class RpcSchemaError(BadRequest):
    def __init__(self, message=None):
        if not message:
            message = 'RPC validation failed'
        super().__init__(message)
