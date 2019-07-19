from inspect import stack
from json import loads
from requests import get
from .errors import raise_error


class ApiModule:
    __slots__ = ('_params', '_url', '_throwing_errors', '_raw_response')

    def __init__(self, params, url, throwing_errors, raw_response):
        self._params = params
        self._url = url
        self._throwing_errors = throwing_errors
        self._raw_response = raw_response

    def _get_response(self, variables):
        method_name = stack()[1][3]
        params = self._params.copy()
        del variables['self']
        for key, value in variables.items():
            if str(value) != 'None':
                data = ['_global', '_type', '_filter', '_id', '_hash', '_object']
                if key in data:
                    key = key[1:]
                params.update({key: value})
        response = loads(get(f'{self._url}.{method_name}', params).text)
        if 'error' in response and self._throwing_errors:
            error_msg = response['error']['error_msg']
            raise_error(error_msg)
        elif self._raw_response:
            return response.get('response', response.get('error'))
        else:
            return ApiResponse(response.get('response', response.get('error')))

    def _get_response2(self, variables):
        params = self._params.copy()
        del variables['self']
        for key, value in variables.items():
            if str(value) != 'None':
                data = ['_global', '_type', '_filter', '_id', '_hash', '_object']
                if key in data:
                    key = key[1:]
                params.update({key: value})
        response = loads(get(f'{self._url}', params).text)
        if 'error' in response and self._throwing_errors:
            error_msg = response['error']['error_msg']
            raise_error(error_msg)
        elif self._raw_response:
            return response.get('response', response.get('error'))
        else:
            return ApiResponse(response.get('response', response.get('error')))


def get_response(url, params, throwing_errors, raw_response):
    response = loads(get(url, params).text)
    if 'error' in response and throwing_errors:
        error_msg = response['error']['error_msg']
        raise_error(error_msg)
    elif raw_response:
        return response.get('response', response.get('error'))
    else:
        return ApiResponse(response.get('response', response.get('error')))


class ApiResponse:
    def __init__(self, params):
        if type(params) is dict:
            self.__dict__ = params
        else:
            self.__dict__ = {'response': params}

    def getAttrs(self):
        return self.__dict__
