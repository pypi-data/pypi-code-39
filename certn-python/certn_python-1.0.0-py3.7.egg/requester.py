import json
from functools import partial
from http import HTTPStatus

import requests

from certn.errors import APIError


ALLOWED_METHODS = {'post', 'get', 'put', 'delete'}
DEFAULT_TIMEOUT = 10


try:
    from json.decoder import JSONDecodeError
except ImportError:
    # json parsing throws a ValueError in python2
    JSONDecodeError = ValueError


def _requests_http_request(url, method, data, headers, auth=None, timeout=DEFAULT_TIMEOUT):
    '''Send HTTP request to given url using the method.'''
    normalized_method = method.lower()

    # headers.update({'User-Agent': 'Python v{}'.format(__version__)})
    if normalized_method in ALLOWED_METHODS:
        if auth:
            return getattr(requests, normalized_method)(
                url, json=data, headers=headers, timeout=timeout, auth=auth
            )
        return getattr(requests, normalized_method)(
            url, json=data, headers=headers, timeout=timeout
        )
    else:
        raise Exception('Invalid request method {}'.format(method))


def raise_on_error(response):
    '''Check response codes and raises corresponding error'''
    if response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED]:
        raise APIError.from_response(
            {
                'error_message': response.text,
                'error_type': 'INVALID_REQUEST',
                'error_code': response.status_code,
                'display_message': None,
                'request_id': '',
                'causes': [],
            }
        )

    # TODO: Retry logic for this case
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        raise APIError.from_response(
            {
                'error_message': response.text,
                'error_type': 'API_ERROR',
                'error_code': response.status_code,
                'display_message': None,
                'request_id': '',
                'causes': [],
            }
        )


def translate_response(response, is_json):
    '''Translate the response to plaintext'''
    if is_json or response.headers['Content-Type'] == 'application/json':
        try:
            response_body = json.loads(response.text) if response.text else response.text
        except JSONDecodeError:
            raise APIError.from_response(
                {
                    'error_message': response.text,
                    'error_type': 'API_ERROR',
                    'error_code': 'INTERNAL_SERVER_ERROR',
                    'display_message': None,
                    'request_id': '',
                    'causes': [],
                }
            )

        # NOTE: top level primitives is valid json.
        if type(response_body) == dict and response_body.get('error_type'):
            raise APIError.from_response(response_body)
        else:
            return response_body
    else:
        return response.content


def http_request(
    url,
    method=None,
    data=None,
    headers=None,
    is_json=True,
    auth=None,
    timeout=DEFAULT_TIMEOUT,
):
    '''Send a http request, check for errors and translate to json object'''
    response = _requests_http_request(
        url=url,
        method=method,
        data=data or {},
        headers=headers or {},
        auth=auth or None,
        timeout=timeout,
    )

    raise_on_error(response)

    return translate_response(response, is_json)


# helpers to simplify partial function application
post_request = partial(http_request, method='POST')
get_request = partial(http_request, method='GET')
put_request = partial(http_request, method='PUT')
delete_request = partial(http_request, method='DELETE')
