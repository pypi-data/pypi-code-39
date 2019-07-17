import functools
import inspect
from asyncio import Future, get_running_loop

__all__ = ['RpcException', 'get_service_proxy']

class RpcException(Exception):
    pass

class RpcProxy:
    def __init__(self, transporter, service_name, loop=None):
        self.loop = loop if loop else get_running_loop()
        self.transporter = transporter
        self.ns = service_name
        self.seq = 1
        self.futures = {}

    def _on_rpc_return(self, seq, value, error):
        future = self.futures.get(seq)
        if not future:
            return

        if error:
            future.set_exception(RpcException(error))
        else:
            future.set_result(value)

        del self.futures[seq]

    async def __rpc_call(self, method, *params):
        em = self.transporter.emit('__rpc_call__', {
            'ns': self.ns,
            'seq': self.seq,
            'method': method,
            'params': params
        })
        if inspect.isawaitable(em):
            await em

        future = self.loop.create_future()
        self.futures[self.seq] = future
        self.seq = self.seq + 1
        return await future

    async def __rpc_call_no_ret(self, method, callback, *params):
        em = self.transporter.emit('__rpc_call__', {
            'ns': self.ns,
            'seq': 0,
            'method': method,
            'params': params
        })
        if inspect.isawaitable(em):
            await em

    def __getattr__(self, method):
        func = functools.partial(self.__rpc_call, method)
        func.noret = functools.partial(self.__rpc_call_no_ret, method)
        setattr(self, method, func)
        return func

def ensure_rpc_proxy(transporter):
    proxies = getattr(transporter, '__rpc_proxies', None)
    if proxies:
        return proxies
    proxies = {}
    transporter.__rpc_proxies = proxies

    def on_rpc_return(data):
        proxy = proxies.get(data['ns'])
        if not proxy:
            return
        proxy._on_rpc_return(data['seq'], data.get('value'), data.get('error'))

    transporter.on('__rpc_return__', on_rpc_return)
    return proxies

def get_service_proxy(transporter, service_name, event_loop=None):
    proxies = ensure_rpc_proxy(transporter)
    proxy = proxies.get(service_name)
    if proxy:
        return proxy
    proxy = RpcProxy(transporter, service_name, event_loop)
    proxies[service_name] = proxy
    return proxy
