from falcon import Response, Request, HTTP_200
from typing import Any
from .json_rpc import JsonRpcRequest, JsonRpcResponse
from .errors import JsonDecodingError
from .validators import validate_json_rpc_request
from .util import json_encode, update_config
from .config import config, InjectedAttributes
import json
# from .logging import logger
from logging import getLogger

logger = getLogger(__name__)


def _read_json_stream(req: Request) -> Any:
    req.context[InjectedAttributes.context_json_data] = {}
    if req.content_length:
        raw = None
        try:
            raw = req.stream.read().strip()
            req.context[InjectedAttributes.context_json_data] = json.loads(raw.decode('utf-8'))
        except UnicodeDecodeError:
            raise JsonDecodingError('Wrong request encoding. Must be UTF-8.')
        except ValueError:
            logger.exception(f'JSON syntax error, raw data: {raw}.')
            raise JsonDecodingError(f'JSON syntax error.')
        except BaseException as e:
            logger.exception(f'JSON parse unknown error.')
            raise JsonDecodingError(f'JSON parse error.')


def _is_rpc_enabled(resource) -> bool:
    return getattr(resource, InjectedAttributes.enable_json_rpc, False)


def _is_json_exchange(resource) -> bool:
    return getattr(resource, InjectedAttributes.json_exchange_flag, False)


class JsonRpcMiddleware(object):

    def __init__(self, **kwargs):
        update_config(**kwargs)

    def process_resource(self, req, resp, resource, params):
        if _is_json_exchange(resource):
            _read_json_stream(req)
            if _is_rpc_enabled(resource):
                if req.method.lower() == 'post':
                    if config.auto_validate_json_rpc_request:
                        validate_json_rpc_request(req)
                req.context[InjectedAttributes.context_json_data] = JsonRpcRequest(req)

    def process_response(self, req: Request, resp: Response, resource: Any, req_succeeded: bool):
        # logger.debug(f'Response is {resp.__dict__}')
        # logger.debug(f'Response body is {resp.body}')
        json_result = getattr(resp, InjectedAttributes.context_json_data, None)
        if json_result is not None:
            if _is_rpc_enabled(resource):
                resp.body = JsonRpcResponse(req, result=json_result).to_json(False)
            else:
                resp.body = json_result
            # logger.debug(resp.body)
            resp.body = json_encode(resp.body)


class CorsMiddleware:

    def __init__(self, allow_origin: str = '*', max_age: int = 86400):
        self.allow_origin = allow_origin
        self.max_age = max_age

    def process_response(self, req, resp, resource, req_succeeded):
        if not self.allow_origin or not len(self.allow_origin):
            return
        resp.set_header('Access-Control-Allow-Origin', self.allow_origin)
        if (req_succeeded
                and req.method == 'OPTIONS'
                and req.get_header('Access-Control-Request-Method')
        ):
            # NOTE: This is a CORS preflight request. Patch the response accordingly.
            allow = resp.get_header('Allow')
            resp.delete_header('Allow')
            allow_headers = req.get_header('Access-Control-Request-Headers', default='*')
            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', self.max_age),
            ))
