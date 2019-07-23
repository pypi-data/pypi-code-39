from typing import Dict, Any, Union, List
from functools import partial
import types
import jsonschema
from ..exceptions import RpcSchemaError
import inspect
from .config import Config
import os


class RpcEntryPoint:

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        inst.__params = (args, kwargs)
        return inst

    def __init__(self, name: str, **kwargs):
        self.pid = os.getpid()
        self.name = name
        self.method_name = None
        self.method_container = None
        self.validation_schema = kwargs['schema'] if 'schema' in kwargs else None
        self.validation_error_code = None
        self.__params = None

    def call(self, params: Union[Dict[str, Any], List[Any]] = None):
        args = []
        kwargs = {}
        if params:
            if type(params) is list:
                args = params
            else:
                kwargs = params

        # logger.debug(f'RPC entry `{self.method_container.name}.{self.name}` <PID {self.pid}> called with '
        #              f'args <{args}> and kwargs <{kwargs}>.')

        if self.validation_schema:
            if len(args):
                validate_json_rpc_data(list(args), self.validation_schema, RpcSchemaError)
            elif len(kwargs):
                validate_json_rpc_data(kwargs, self.validation_schema, RpcSchemaError)
        self.check_signature(args, kwargs)
        return getattr(self.method_container, self.method_name)(*args, **kwargs)

    def bind(self, method_container, method_name):
        if not hasattr(method_container, Config.rpc_methods_injected_attr):
            raise RuntimeError(f'Cannot bind RPC method `{method_name}`. '
                               f'Class `{method_container.__class__.__name__}` must have '
                               f'`{Config.rpc_methods_injected_attr}<dict>` attribute.')
        if self.is_bound():
            raise RuntimeError(f'Cannot bind already bound entry point `{method_name}` as `{self.name}`.')
        instance = self
        instance.method_name = method_name
        instance.method_container = method_container
        container_rpc_methods = getattr(instance.method_container, Config.rpc_methods_injected_attr)
        container_rpc_methods[self.name] = instance
        instance.pid = os.getpid()
        return instance

    def is_bound(self):
        return self.method_container is not None

    def check_signature(self, args, kwargs):
        fn = getattr(self.method_container, self.method_name)
        try:
            inspect.getcallargs(fn, *args, **kwargs)
        except TypeError as exc:
            raise RpcSchemaError(f'Wrong method signature. {str(exc)}')
        except Exception as exc:
            raise RpcSchemaError(f'Checking method signature failed. {str(exc)}')

    @classmethod
    def rpc_entry_point(cls, *decoargs, **decokwargs):
        """
        Decorator for RPC methods. Only instance methods can be decorated.

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
            setattr(fn, Config.rpc_entry_point_attr, instance)
            return fn

        if len(decoargs) == 1 and isinstance(decoargs[0], types.FunctionType):
            return wrapped_f(decoargs[0], args=(), kwargs={})
        else:
            return partial(wrapped_f, args=decoargs, kwargs=decokwargs)


rpc_entry_point = RpcEntryPoint.rpc_entry_point


def _is_entrypoint(method):
    return hasattr(method, Config.rpc_entry_point_attr)


def validate_json_rpc_data(data: Any, schema: Any, exception_cls: type = RpcSchemaError):
    try:
        jsonschema.validate(data, schema, format_checker=jsonschema.FormatChecker())
    except jsonschema.ValidationError as e:
        raise exception_cls(e.message)


def get_entrypoint(method):
    if _is_entrypoint(method):
        return getattr(method, Config.rpc_entry_point_attr, None)
    return None
