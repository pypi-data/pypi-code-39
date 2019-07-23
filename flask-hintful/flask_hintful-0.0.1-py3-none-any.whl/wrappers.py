from functools import wraps

from flask import Response, request

from .serializing import serialize
from .utils import get_args_from_request


def view_func_wrapper(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        '''Validates and parses View args, Query args, or body input to the function'''
        kwargs = get_args_from_request(view_func, request)

        rv = view_func(**kwargs)

        if isinstance(rv, tuple):
            headers = {}
            status = None

            if len(rv) == 3:
                body, status, headers = rv
            elif len(rv) == 2:
                if isinstance(rv[1], (int, str)):
                    body, status = rv
                else:
                    body, headers = rv

            if headers is None or headers.get('Content-Type') is None:
                headers['Content-Type'] = 'application/json'

            if status is not None:
                return serialize(body), status, headers
            else:
                return serialize(body), headers

        elif isinstance(rv, Response):
            rv.data = serialize(rv.get_data(as_text=True))
            if rv.headers is None or rv.headers.get('Content-Type') is None:
                rv.headers['Content-Type'] = 'application/json'
            return rv
        return serialize(rv), {'Content-Type': 'application/json'}
    return decorator


class BlueprintWrapper():

    def __init__(self, flask_hintful_api):
        self.flask_hintful_api = flask_hintful_api

    def add_url_rule(self, rule, endpoint, view_func, **options):
        wrapped_view_func = view_func_wrapper(view_func)
        self.flask_hintful_api._add_openapi_path(
            rule, options.get('methods', ['GET']), view_func)
        return lambda s: s.add_url_rule(rule, endpoint, wrapped_view_func, **options)
