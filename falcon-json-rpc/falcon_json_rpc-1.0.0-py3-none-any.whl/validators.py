import jsonschema
from typing import Any
from .errors import JsonRpcSchemaError

JsonRpcRequestSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "A JSON RPC 2.0 request",
    "oneOf": [
        {
            "description": "An individual request",
            "$ref": "#/definitions/request"
        },
        {
            "description": "An array of requests",
            "type": "array",
            "items": {"$ref": "#/definitions/request"},
            "minItems": 1
        }
    ],
    "definitions": {
        "request": {
            "type": "object",
            "required": ["jsonrpc", "method"],
            "properties": {
                "jsonrpc": {"enum": ["2.0"]},
                "method": {
                    "type": "string"
                },
                "id": {
                    "type": ["string", "number"]
                },
                "params": {
                    "type": ["array", "object"]
                }
            }
        }
    }
}


def validate_json_rpc_data(data: Any, schema: Any, exception_cls: type = JsonRpcSchemaError):
    try:
        jsonschema.validate(data, schema, format_checker=jsonschema.FormatChecker())
    except jsonschema.ValidationError as e:
        raise exception_cls(e.message)


def validate_json_rpc_request(req):
    if not 'json' in req.context:
        raise JsonRpcSchemaError('Context does not contain `json`. '
                                 'Perhaps, middleware was not initialized')
    validate_json_rpc_data(req.context['json'], JsonRpcRequestSchema, JsonRpcSchemaError)
