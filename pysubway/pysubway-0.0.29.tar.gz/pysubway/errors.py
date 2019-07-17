class IncomingDataError(Exception):
    pass


class IncomingDataTypeError(IncomingDataError):
    pass


class IncomingDataValueError(IncomingDataError):
    pass


class RequestFailed(Exception):
    pass