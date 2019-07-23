import falcon
from typing import Dict, Any, List
from .json_rpc_router import JsonRpcRouter
from .middleware import CorsMiddleware, JsonRpcMiddleware
from .util import update_config
from .config import get_config
from logging import getLogger

logger = getLogger(__name__)


class JsonRpcServer:

    def __init__(self, routes: Dict[str, str] = None,
                 config: Dict[str, Any] = None,
                 middleware: List[Any] = None) -> falcon.API:
        """

        :param routes: Dictionary of JSON RPC API routes in format {`route`: `methods_module_path`}
        :param config: Global configuration, check available options in `config.py`
        :param middleware: List of middleware to be passed to `falcon` application
        """
        self.falcon: falcon.API = None
        self.middleware: List[Any] = middleware if middleware else list()
        self.routers: Dict[str, JsonRpcRouter] = {}
        self.routes: Dict[str, str] = routes or {}

        if config:
            update_config(**config)
        self.config = get_config()
        self._setup_falcon()

    def _setup_falcon(self):
        add_json_rpc_middleware = True
        add_cors_middleware = self.config.access_control_allow_origin and len(self.config.access_control_allow_origin)

        for m in self.middleware:
            if type(m) is JsonRpcMiddleware:
                add_json_rpc_middleware = False
                logger.warning(f'{type(m).__name__} was initialized in main application. '
                               'This step is not required, it would be passed to falcon anyway.')
            if type(m) is CorsMiddleware:
                add_cors_middleware = False
                logger.warning(f'{type(m).__name__} was initialized in main application. '
                               'This step is not required, instead you could use configuration '
                               'options `access_control_allow_origin` amd/or `access_control_max_age`')

        if add_json_rpc_middleware:
            self.middleware.append(JsonRpcMiddleware())
        if add_cors_middleware:
            self.middleware.append(CorsMiddleware(self.config.access_control_allow_origin,
                                                  self.config.access_control_max_age))
        self.falcon = falcon.API(middleware=self.middleware)
        self.bind_routes(self.routes)

    def bind_routes(self, routes: Dict[str, str]):
        for route, methods_path in routes.items():
            logger.debug(f'Binding route `{route}` to `{methods_path}`.')
            self.routers[route] = JsonRpcRouter(self.falcon, route, methods_path)

    @property
    def application(self):
        return self.falcon
