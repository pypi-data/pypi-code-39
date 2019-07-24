from asyncio import AbstractEventLoop
from logging import Logger, getLogger
from typing import Callable, Dict, Optional


class FatalError(Exception):
    pass


def fatal_error_handler(
    func: Callable[[], None], logger: Optional[Logger] = None
) -> Callable[[AbstractEventLoop, Dict], None]:
    """Returns asyncio event loop exception handler that logs the exception context
    and calls func if exception represents a FatalError.

    :param Callable[[], None] func: Function to call on FatalError.
    :param Logger, optional logger: Exception logger, defaults to root logger.
    :return Callable[[AbstractEventLoop, Dict], None]: Asyncio event loop exception handler.
    """
    _logger = logger or getLogger()

    def handler(loop: AbstractEventLoop, context: Dict):
        message = context.get("message")
        exc: Optional[Exception] = context.get("exception")

        is_fatal_error = isinstance(exc, FatalError)

        error_type = "FATAL ERROR" if is_fatal_error else "Error"
        _logger.error(
            f"{error_type} in event loop: message={message}, exc={exc}",
            exc_info=exc,
            extra={"context": context},
        )

        if is_fatal_error:
            func()

    return handler
