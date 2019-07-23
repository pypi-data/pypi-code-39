import inspect
import types
import re
from typing import Dict, Any, Union, List, Callable
from falcon import Request, HTTPError
from functools import partial
from .config import config, InjectedAttributes
from .util import json_encode
from .validators import validate_json_rpc_data
from .errors import JsonRpcParamsError, JsonRpcMethodCallError, JsonRpcError
from logging import getLogger
import pkgutil

logger = getLogger(__name__)

JsonRpcParams = Union[None, Dict[str, Any], List[Any]]


def _register_entrypoint(fn, entrypoint):
    descriptors = getattr(fn, InjectedAttributes.entry_point, None)
    if descriptors is None:
        descriptors = set()
        setattr(fn, InjectedAttributes.entry_point, descriptors)
    descriptors.add(entrypoint)


def json_rpc_entrypoint_container_extractor(module):
    def is_entrypoint(method):
        return hasattr(method, InjectedAttributes.entry_point)

    containers = list()
    for _, maybe_container in inspect.getmembers(module, lambda obj: isinstance(obj, type)):
        if inspect.getmembers(maybe_container, is_entrypoint):
            containers.append(maybe_container)
    return containers


class JsonRpcEntryPoint:
    name = None
    method_name = None
    router = None
    method_container = None
    validation_schema = None
    validation_error_code = None
    __params = None

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        inst.__params = (args, kwargs)
        return inst

    def __init__(self, name: str, **kwargs):
        self.name = name
        if 'schema' in kwargs:
            self.validation_schema = kwargs['schema']

    def call(self, params: Union[Dict[str, Any], List[Any]] = None):
        args = []
        kwargs = {}
        if params:
            if type(params) is list:
                args = params
            else:
                kwargs = params

        if self.validation_schema:
            if len(args):
                validate_json_rpc_data(list(args), self.validation_schema, JsonRpcParamsError)
            elif len(kwargs):
                validate_json_rpc_data(kwargs, self.validation_schema, JsonRpcParamsError)
        self.check_signature(args, kwargs)
        try:
            return getattr(self.method_container, self.method_name)(*args, **kwargs)
        except JsonRpcError:
            raise
        except Exception as e:
            err_descr = f'Internal error during calling method `{self.method_name}`.'
            logger.error(err_descr, exc_info=True)
            raise JsonRpcMethodCallError(err_descr)

    def bind(self, router, method_container, method_name):
        def clone(prototype):
            if prototype.is_bound():
                raise RuntimeError(f'Cannot bind already bound entry point `{method_name}`.')

            cls = type(prototype)
            args, kwargs = prototype.__params
            instance = cls(*args, **kwargs)
            instance.router = router
            try:
                instance.method_container = method_container()
            except Exception as e:
                if str(e).__contains__('required positional argument'):
                    raise Exception(f'Class-container of JSON RPC method `{method_name}` '
                                    'must not have required initialization arguments.')
                # instantiation raised an exception, throw it as it is
                raise

            return instance

        instance = clone(self)
        instance.method_name = method_name
        return instance

    def is_bound(self):
        return self.method_container is not None

    def check_signature(self, args, kwargs):
        fn = getattr(self.method_container, self.method_name)
        try:
            inspect.getcallargs(fn, *args, **kwargs)
        except TypeError as exc:
            raise JsonRpcParamsError(f'Wrong method signature. {str(exc)}')
        except Exception as exc:
            raise JsonRpcParamsError(f'Checking method signature failed. {str(exc)}')

    @classmethod
    def decorator(cls, *decoargs, **decokwargs):
        """
        Decorator for JSON RPC methods. Only instance methods can be decorated.

        :param decoargs: If first argument is provided, it is used as method name.
        :param decokwargs: If 'name' key is provided, it is used as method name.
        :return:
        """

        def wrapped_f(fn, args, kwargs):
            name = decokwargs.get('name', fn.__name__)
            if not (len(decoargs) == 1 and isinstance(decoargs[0], types.FunctionType)):
                if len(args) >= 1:
                    name = args[0]
                    args = args[1:]

            instance = cls(name, *args, **kwargs)
            descriptors = getattr(fn, InjectedAttributes.entry_point, None)
            if not descriptors:
                descriptors = set()
                setattr(fn, InjectedAttributes.entry_point, descriptors)
            descriptors.add(instance)
            return fn

        if len(decoargs) == 1 and isinstance(decoargs[0], types.FunctionType):
            return wrapped_f(decoargs[0], args=(), kwargs={})
        else:
            return partial(wrapped_f, args=decoargs, kwargs=decokwargs)


class JsonRpcResponseError:

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class JsonRpcRequest:

    def __init__(self, req: Request = None):
        a = InjectedAttributes.context_json_data
        json = req.context[a] if req and hasattr(req, 'context') and a in req.context else {}
        self.jsonrpc: str = json.get('jsonrpc', None)
        self.id: str = json.get('id', None)
        self.method: str = json.get('method', None)
        self.params: JsonRpcParams = json.get('params', None)
        self.original_request: Request = req


class JsonRpcResponse:

    def __init__(self, req: Request, result: Any = None, error: JsonRpcResponseError = None):
        self._request_data: JsonRpcRequest = self._get_request_data(req)
        self.jsonrpc: str = self._request_data.jsonrpc if self._request_data else config.json_rpc_version
        self.id: str = self._request_data.id if self._request_data else None
        self.result: Any = result
        self.error: JsonRpcResponseError = error

    def to_json(self, encode=True):
        o = {'jsonrpc': self.jsonrpc, 'id': self.id}
        if self.error is not None:
            o['error'] = {'code': self.error.code, 'message': self.error.message}
        if self.result is not None and self.error is None:
            o['result'] = self.result
        if self.result is None and self.error is None:
            o['result'] = None
        if not encode:
            return o
        return json_encode(o)

    def _get_request_data(self, req: Request) -> JsonRpcRequest:
        a = InjectedAttributes.context_json_data
        return req.context[a] if req and hasattr(req, 'context') and a in req.context else None


JsonRpcMethod = JsonRpcEntryPoint.decorator
