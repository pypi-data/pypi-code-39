import asyncio
import random
import time
from contextlib import AbstractContextManager
from functools import wraps
from typing import Any, Callable, Type, TypeVar, Union

T = TypeVar("T")

# Decorators to preserve function signature using this pattern:
# https://github.com/python/mypy/issues/1927
FuncT = TypeVar("FuncT", bound=Callable[..., Any])


class reraise(AbstractContextManager):
    """
    Context manager to reraise one exception from another
    """

    def __init__(self, exc_a: Type[Exception], exc_b: Type[Exception]):
        self.exc_a = exc_a
        self.exc_b = exc_b

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and issubclass(exc_type, self.exc_a):
            raise self.exc_b from exc_value

    def __call__(self, func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def decorated(*args, **kwargs):
                with self:
                    return await func(*args, **kwargs)

            return decorated

        @wraps(func)
        def decorated(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return decorated


def retry_on_exception(  # noqa: C901
    exc: Union[Exception, Type[Exception]], wait: int, tries: int
):
    """
    Decorator to retry a function if an exception `exc` occurs.
    :param exc: Exception to catch.
    :param wait: Random wait between 0 and `wait` seconds between retries.
    :param tries: Number of retries. Set to -1 for infinite retries.
    """

    def decorator(func: FuncT) -> FuncT:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_decorated(*args, **kwargs):
                attempt = tries
                while attempt != 0:
                    attempt -= 1
                    try:
                        return await func(*args, **kwargs)
                    except exc:
                        if attempt == 0:
                            raise exc
                    if wait:
                        await asyncio.sleep(random.random() * wait)

            return async_decorated  # type: ignore

        @wraps(func)
        def decorated(*args, **kwargs):
            attempt = tries
            while attempt != 0:
                attempt -= 1
                try:
                    return func(*args, **kwargs)
                except exc:
                    if attempt == 0:
                        raise exc
                if wait:
                    time.sleep(random.random() * wait)

        return decorated  # type: ignore

    return decorator
