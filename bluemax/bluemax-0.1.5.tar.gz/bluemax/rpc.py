"""
    We want to provide a remote procedure context
"""
import asyncio
import functools
import importlib
import logging
from concurrent.futures import ThreadPoolExecutor
from .asyncpoolexecutor import AsyncPoolExecutor
from . import context


LOGGER = logging.getLogger(__name__)


class Rpc:
    """ Base class for rpcs """

    def __init__(self, package, *args, **kwargs):
        """ Given a package """
        self._package_ = package
        LOGGER.info("rpc package available: %s", self._package_)

    @property
    def procedures(self):
        """ return a list of publicly available functions """
        return getattr(self._package_, "__all__")

    def perform(self, qname, *args, **kwargs):
        """ perform the function and result the result """
        LOGGER.debug("perform: %s", qname)
        func = getattr(self._package_, qname)
        result = func(*args, **kwargs)
        return result

    def broadcast(self, signal, message, client_filter=None):
        """ subclass responsibly: noop! """

    def broadcast_later(self, messages):
        """ subclass responsibly: noop! """

    @classmethod
    def rpc_for(cls, module_name, *args, **kwargs):
        """ will import a module_name and return an rpc """
        LOGGER.info("loading module: %s", module_name)
        package = importlib.import_module(module_name)
        return cls(package, *args, **kwargs)


class AsyncRpc(Rpc):
    """ We need to perform async function """

    async def perform(self, qname, *args, **kwargs):
        """ If the result is a coro - await it """
        result = super().perform(qname, *args, **kwargs)
        if asyncio.iscoroutine(result):
            LOGGER.debug("awaiting: %s", qname)
            result = await result
        return result


class PoolRpc(AsyncRpc):
    """
        We can restrict the number of workers
    """

    def __init__(self, *args, max_workers=None, max_threads=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._thread_pool_ = ThreadPoolExecutor(max_workers=max_threads)
        self._async_pool_ = AsyncPoolExecutor(max_workers=max_workers)
        self._async_pool_.start()
        self._loop = asyncio.get_event_loop()

    def perform(self, qname, *args, **kwargs):
        """ Submit func to the right pool """
        func = getattr(self._package_, qname)
        if asyncio.iscoroutinefunction(func):
            pool = self._async_pool_
        else:
            pool = self._thread_pool_
        proc = functools.partial(func, *args, **kwargs)
        future = self._loop.run_in_executor(pool, proc)
        return future

    async def shutdown(self, wait=True):
        """ We have runnning resources that require tidy up """
        self._thread_pool_.shutdown(wait=wait)
        await self._async_pool_.shutdown(wait=wait)
        LOGGER.info("shutdown")


class BroadcastMixin:
    """ How we get the message out """

    def get_broadcast_queue(self):
        """ returns the queue containing signals for clients """
        return self._broadcast_q_

    def _broadcast_(self, signal, message, client_filter=None):
        """ Add message to broadcast queue """
        LOGGER.debug("queuing broadcast: %s", message)
        self._broadcast_q_.put_nowait((signal, message, client_filter))

    def broadcast(self, signal, message, client_filter=None):
        """ Add message to broadcast queue thread safe"""
        self._loop.call_soon_threadsafe(
            self._broadcast_, signal, message, client_filter
        )

    def broadcast_later(self, messages):
        """ Will add messages from any thread back to our _loop """
        for message in messages:
            self._loop.call_soon_threadsafe(self._broadcast_, *message)


class ContextRpc(BroadcastMixin, PoolRpc):
    """
        We execute in a context
    """

    def __init__(self, *args, **kwargs):
        """ introduce a broadcast queue """
        context._MANAGER_ = self  # pylint: disable=W0212
        self._broadcast_q_ = asyncio.Queue()
        super().__init__(*args, **kwargs)

    def qname_to_func(self, qname):
        """ return the function for the qname """
        return getattr(self._package_, qname)

    def perform(self, user, qname, *args, **kwargs):  # pylint: disable=W0221
        """ Submit func to the right pool and context """

        func = self.qname_to_func(qname)
        logging.debug("calling %s", func)
        if asyncio.iscoroutinefunction(func):
            pool = self._async_pool_
            proc = functools.partial(context.acontext_call, func, user, args, kwargs)
        else:
            pool = self._thread_pool_
            proc = functools.partial(context.context_call, func, user, args, kwargs)
        future = self._loop.run_in_executor(pool, proc)
        return future
