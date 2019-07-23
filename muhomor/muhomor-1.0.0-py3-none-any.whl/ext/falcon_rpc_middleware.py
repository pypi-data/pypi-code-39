import os
from logging import getLogger
from ..rpc.config import configure
from ..rpc.worker import RpcClient


logger = getLogger(__name__)


class FalconRpcMiddleware:

    def __init__(self, service_name: str, **config):
        if config:
            configure(**config)
        logger.debug(f'Initializing RPC Client, PID {os.getpid()}')
        self.rpc = RpcClient(service_name)

    def process_resource(self, req, resp, resource, params):
        resource.rpc = self.rpc

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'rpc'):
            pass


