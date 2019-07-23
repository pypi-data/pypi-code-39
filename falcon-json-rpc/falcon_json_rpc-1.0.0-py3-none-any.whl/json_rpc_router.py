from falcon import Response, Request, API
from typing import Callable, Dict, Any, List
from .errors import JsonRpcError, JsonRpcMethodNotFoundError, JsonRpcMethodCallError
from muhomor.utils.filesystem import decorator_containers_from_module
from .json_rpc import (
    json_rpc_entrypoint_container_extractor,
    JsonRpcRequest,
    JsonRpcParams
)
import inspect
import os
from logging import getLogger
from .serializers import error_serializer
from .config import InjectedAttributes
from .decorators import JsonRpc

logger = getLogger(__name__)


@JsonRpc
class JsonRpcRouter:

    def __init__(self, application: API, entry_point: str, methods_path: str):
        self._setup(application, entry_point, methods_path)
        self._setup_application()

    def _setup(self, application: API, entry_point: str, methods_path: str):
        self.application = application
        self.methods: Dict[str, Callable] = {}
        self.registered_method_names: List[str] = list()
        self.entry_point = entry_point
        self.methods_path = methods_path
        self.method: str = None
        self.params: JsonRpcParams = None
        self.data: JsonRpcRequest = JsonRpcRequest()
        self._register_methods(self.methods_path)

    def _setup_application(self):
        self.application.set_error_serializer(error_serializer)
        self.application.add_route(self.entry_point, self)

    def _register_methods(self, methods_path: str):
        method_containers = decorator_containers_from_module(methods_path, json_rpc_entrypoint_container_extractor)
        for container in method_containers:
            for method_name, method in inspect.getmembers(container, inspect.isfunction):
                entrypoints = getattr(method, InjectedAttributes.entry_point, [])
                for entrypoint in entrypoints:
                    if entrypoint.name in self.methods:
                        raise Exception(f'JSON-RPC method {entrypoint.name} is registered already')
                    bound = entrypoint.bind(self, container, method_name)
                    setattr(container, 'resource', self)
                    self.methods[entrypoint.name.lower()] = bound.call
                    self.registered_method_names.append(entrypoint.name.lower())

    def _call(self, method, params):
        logger.debug(f'JSON RPC router methods in PID {os.getpid()}: {self.registered_method_names}')
        if method not in self.registered_method_names:
            raise JsonRpcMethodNotFoundError(f'Method {method} is not available')
        return self.methods[method](params)

    def on_post(self, req: Request, resp: Response):
        try:
            j: JsonRpcRequest = req.context[InjectedAttributes.context_json_data]
            result = self._call(j.method.lower(), j.params)
            setattr(resp, InjectedAttributes.context_json_data, result)
        except JsonRpcError:
            logger.exception('Error `JsonRpcError` calling JSON RPC method')
            raise
        except BaseException:
            logger.exception('Error calling JSON RPC method')
            raise

    def on_get(self, req: Request, resp: Response):
        pass

    def on_put(self, req: Request, resp: Response):
        pass

    def on_patch(self, req: Request, resp: Response):
        pass

    def on_options(self, req: Request, resp: Response):
        pass
