# TO-DO: ACCESS CONFIG ONNLY THROUGH GET_CONFIG


class Config:

    def __init__(self):
        self.json_rpc_version: str = "2.0"
        self.enable_json_rpc: bool = True
        self.auto_validate_json_rpc_request: bool = True

        # set to None or empty string do disable
        self.access_control_allow_origin: str = None
        # in seconds
        self.access_control_max_age: int = 86400  # 24 hours


class ErrorCodes:

    def __init__(self):
        self.json_decoding: int = -77001
        self.json_encoding: int = -77002
        self.json_rpc_schema_validation: int = -77003
        self.json_rpc_params_validation: int = -77004
        self.json_rpc_unavailable_method: int = -77005
        self.json_rpc_method_call: int = -77006
        self.json_rpc_method_not_found: int = -77007


class InjectedAttributes:
    entry_point: str = 'json_rpc_methods'
    context_json_data: str = 'json'
    json_exchange_flag: str = 'json_exchange'
    enable_json_rpc: str = 'enable_json_rpc'


config = Config()

error_codes = ErrorCodes()


def get_error_codes() -> ErrorCodes:
    return error_codes


def get_config() -> Config:
    return config
