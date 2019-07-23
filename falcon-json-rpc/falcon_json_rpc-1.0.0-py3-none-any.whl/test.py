from . import FalconJsonRpcMiddleware, error_serializer

mw = FalconJsonRpcMiddleware(as_json_rpc=True, auto_validate_json_rpc_request=True)

print(f'Middleware: {mw}')
