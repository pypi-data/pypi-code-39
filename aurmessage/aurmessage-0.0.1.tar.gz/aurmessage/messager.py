from __future__ import annotations

import asyncio
import functools
import inspect
import logging
import operator
import typing as ty

import aioredis
import jsonpickle
from aioredis import Redis

from aurmessage.mpmc import MPMC

log = logging.getLogger("aurmessage")


def _listify_arg(listy: ty.Optional[ty.Union[str, ty.Iterable[str]]]) -> ty.Iterable:
    if listy is None:
        return []
    list_like__types = list, tuple, set
    if isinstance(listy, list_like__types):
        return listy
    return [listy]


def _parameterize(deco_to_enhance):
    """
    @_parameterize
    def parameterized_deco(func, *deco_args, **deco_kwargs):
    """

    def deco_factory(*args, **kwargs):
        # Factory for decorators that accept a function retaining original arguments
        def deco_wrapper(func):
            # Return result of original deco (a normal deco'd function)
            return deco_to_enhance(func, *args, **kwargs)

        return deco_wrapper

    return deco_factory


@_parameterize
def _link_args(func, *arg_tups):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_binding = inspect.signature(func).bind(*args, **kwargs).arguments
        for arg_tup in arg_tups:
            if functools.reduce(operator.xor, [arg in func_binding for arg in arg_tup]):
                raise ValueError(f"{' and '.join(arg_tup)} must all be defined or undefined")

        func(*args, **kwargs)

    return wrapper


T_m = ty.TypeVar("T_m")


class Messager:
    mpmc: MPMC
    receiver: aioredis.pubsub.Receiver
    redis: Redis

    @_link_args(("serializer", "deserializer"))
    def __init__(self,
                 name="Anon",
                 serializer: ty.Callable[[T_m], ty.Any] = jsonpickle.dumps,
                 deserializer: ty.Callable[[ty.Any], T_m] = jsonpickle.loads):
        self.name = name
        self.serializer = serializer
        self.deserializer = deserializer
        self.waiting_handler_ct = 0
        self.waiting_handlers_done = asyncio.Event()

    async def init(self) -> Messager:
        if self.redis is not None:
            raise RuntimeWarning(f"[{self.name} init called more than once")
        self.redis: aioredis.Redis = await aioredis.create_redis('redis://localhost')
        self.mpmc: MPMC = MPMC(self.redis, serializer=self.serializer, deserializer=self.deserializer)
        self.waiting_handler_ct = 0
        self.waiting_handlers_done.clear()
        await self.mpmc.start()
        await asyncio.sleep(0.1)

        return self

    async def stop(self):
        log.info(f"[{self.name}] Stopping Messager")
        await self.mpmc.stop()
        if self.waiting_handler_ct != 0:
            log.debug(f"[{self.name}] Waiting for {self.waiting_handler_ct} handles to clear")
            await self.waiting_handlers_done.wait()

    async def _handle(self,
                      handler_func: ty.Callable[[T_m], ty.Any],
                      channel: str,
                      is_pattern: bool = False) -> None:

        is_coro = inspect.iscoroutinefunction(handler_func)

        log.info(
            f"[{self.name}][handler] "
            f"Registering {'async' if is_coro else ''} handler {handler_func.__name__} "
            f"for {'channel pattern' if is_pattern else 'channel'} {channel}")
        async for message in self.mpmc.subscribe(channel, is_pattern=is_pattern):
            if is_coro:
                self.waiting_handler_ct += 1
                logging.debug(f"[{self.name}][handler] Handle count: {self.waiting_handler_ct}")
                self.waiting_handlers_done.clear()

                # Callback for handler_funcs that tracks number of ongoing handler_funcs
                def track_live_handlers(_):
                    self.waiting_handler_ct -= 1
                    if self.waiting_handler_ct == 0:
                        logging.debug(f"[{self.name}][handler] Handle count at 0, setting done")
                        self.waiting_handlers_done.set()

                asyncio.create_task(handler_func(message)).add_done_callback(track_live_handlers)
            else:
                handler_func(message)

    def subscribe(self, handler_func: ty.Callable[[T_m], ty.Any],
                  channels: ty.Union[str, ty.List[str]] = None,
                  channel_patterns: ty.Union[str, ty.List[str]] = None) -> ty.Awaitable:
        """
        Usage:
            (async) def handle(message):
                do_something(message)

            (await) Messager().subscribe(handle, "test")
        :param handler_func: Called with message when matching channel received
        :param channels: Channels to accept for handler_func
        :param channel_patterns: Channel patterns to accept for handler_func
        :return: Small sleep to ensure proper handler registration. Optional, but will raise a runtimewarning
        """
        log.info(f"[{self.name}][subscribe] "
                     f"Subscribing to channels [{','.join(channels)}], "
                     f"channel patterns [{','.join(channel_patterns)}] with func {handler_func.__name__}")
        channels = _listify_arg(channels)
        channel_patterns = _listify_arg(channel_patterns)
        for t_channel in channels:
            asyncio.create_task(self._handle(handler_func=handler_func, channel=t_channel, is_pattern=False))
        for t_channel_pattern in channel_patterns:
            asyncio.create_task(self._handle(handler_func=handler_func, channel=t_channel_pattern, is_pattern=True))

        return asyncio.sleep(0.1)

    def publish(self, message: T_m,
                channels: ty.Union[str, ty.List[str]] = None,
                wait: bool = True,
                callback: ty.Optional[ty.Callable[[T_m], ty.Any]] = None) -> ty.Union[ty.Awaitable, ty.Tuple]:
        channels = _listify_arg(channels)
        if wait and callback is not None:
            raise ValueError("Callback provided for awaiting publish")
        pub_coros = [self.mpmc.publish(t_channel, message) for t_channel in channels]
        if wait:
            return asyncio.gather(*pub_coros)
        else:
            if callback:
                for t_coro in pub_coros:
                    asyncio.create_task(t_coro).add_done_callback(lambda x: callback(x.result()))
