r"""Infynipy exception classes.

Includes two main exceptions: :class:`.APIException` for when something goes
wrong on the server side, and :class:`.ClientException` when something goes
wrong on the client side. Both of these classes extend :class:`.InfynipyException`.

"""


class InfynipyException(Exception):
    """The base Infynipy Exception that all other exception classes extend."""


class APIException(InfynipyException):
    """Indicate exception that involve responses from Infynity's API."""

    def __init__(self, status, message):
        """Initialize an instance of APIException.

        :param status: The error code.
        :param message: The associated message for the error.

        .. note:: Calling ``str()`` on the instance returns
            ``unicode_escape``-d ASCII string because the message may be
            localized and may contain UNICODE characters. If you want a
            non-escaped message, access the ``message`` attribute on
            the instance.
        """
        error_str = u"{}: '{}'".format(status, message)
        error_str = error_str.encode("unicode_escape").decode("ascii")

        super(APIException, self).__init__(error_str)
        self.status = status
        self.message = message


class ClientException(InfynipyException):
    """Indicate exceptions that don't involve interaction with Infynity's API."""
