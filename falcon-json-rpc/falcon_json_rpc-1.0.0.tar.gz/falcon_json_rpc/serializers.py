from logging import getLogger
from .json_rpc import JsonRpcResponse, JsonRpcResponseError
from .errors import JsonRpcError

logger = getLogger(__name__)

def error_serializer(req, resp, exception):
    if isinstance(exception, JsonRpcError):
        logger.warning(f'Serializing `JsonRpcError` {exception} {exception.__dict__} into resp.body')
        e = JsonRpcResponseError(exception.code, exception.description)
        inst = JsonRpcResponse(req=req, error=e)
        resp.body = inst.to_json()
    else:
        logger.warning(f'Serializing `UnknownError` {exception} {exception.__dict__} into resp.http_error')
        resp.http_error = exception
    resp.content_type = 'application/json'
    # resp.append_header('Access-Control-Allow-Origin', '*')
