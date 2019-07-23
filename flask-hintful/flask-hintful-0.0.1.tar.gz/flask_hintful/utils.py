from dataclasses import is_dataclass
from inspect import getdoc, signature
from typing import Callable

from werkzeug.datastructures import MultiDict

from .serializing import deserialize


def get_func_metadata(func: Callable) -> dict:
    sig = signature(func, follow_wrapped=False)
    return {
        "return": sig.return_annotation,
        "params": sig.parameters,
        "doc": getdoc(func),
        "empty": sig.empty
    }


def get_args_from_request(view_func, req) -> dict:
    view_func_metadata = get_func_metadata(view_func)
    args = req.args.copy()
    args.update(req.view_args)
    return unmarshall_args(view_func_metadata['params'], args, req.get_json())


def unmarshall_args(params, args: MultiDict, body=None) -> dict:
    parsed_args = {}
    for param_name, param in params.items():
        if param_name in args:
            arg = args.poplist(param_name)
            if param.annotation != param.empty:
                parsed_args[param_name] = deserialize(arg, param.annotation)
            else:
                parsed_args[param_name] = arg if len(arg) > 1 else arg[0]
        else:
            if param.kind == param.VAR_KEYWORD:
                parsed_args.update(args)
            if body is not None:
                if hasattr(param.annotation, '__marshmallow__') or is_dataclass(param.annotation):
                    parsed_args[param_name] = deserialize(
                        body, params[param_name].annotation)
    return parsed_args
