import falcon
from .config import get_config, get_error_codes


# Override `falcon.HTTPError` to include error messages in responses.
class HTTPError(falcon.HTTPError):
    """
    HTTPError that stores a dictionary of validation error messages.
    """

    def __init__(self, status, errors=None, *args, **kwargs):
        self.errors = errors
        super().__init__(status, *args, **kwargs)

    def to_dict(self, *args, **kwargs):
        ret = super().to_dict(*args, **kwargs)
        if self.errors is not None:
            ret['errors'] = self.errors
        return ret


class JsonRpcError(falcon.HTTPError):

    def __init__(self, code: int, description: str = None, status: int = falcon.status.HTTP_200, *args, **kwargs):
        super().__init__(status, code=code, description=description, *args, **kwargs)


class JsonDecodingError(JsonRpcError):

    def __init__(self, description: str = 'JSON decoding failed', *args, **kwargs):
        super().__init__(code=get_error_codes().json_decoding, description=description, *args, **kwargs)


class JsonEncodingError(JsonRpcError):

    def __init__(self, description: str = 'JSON encoding failed', *args, **kwargs):
        super().__init__(code=get_error_codes().json_decoding, description=description, *args, **kwargs)


class JsonRpcSchemaError(JsonRpcError):

    def __init__(self, description: str = 'JSON RPC request validation failed', *args, **kwargs):
        super().__init__(code=get_error_codes().json_rpc_schema_validation, description=description, *args, **kwargs)


class JsonRpcParamsError(JsonRpcError):

    def __init__(self, description: str = 'JSON RPC params validation failed', *args, **kwargs):
        super().__init__(code=get_error_codes().json_rpc_params_validation, description=description, *args, **kwargs)


class JsonRpcMethodNotFoundError(JsonRpcError):

    def __init__(self, description: str = 'This JSON RPC method is not available', *args, **kwargs):
        super().__init__(code=get_error_codes().json_rpc_method_not_found, description=description, *args, **kwargs)


class JsonRpcMethodCallError(JsonRpcError):

    def __init__(self, description: str = 'Internal error. JSON RPC method call failed.', *args, **kwargs):
        super().__init__(code=get_error_codes().json_rpc_method_call, description=description, *args, **kwargs)

