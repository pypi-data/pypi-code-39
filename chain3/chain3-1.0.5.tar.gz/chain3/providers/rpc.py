import logging
import os

from mc_utils import (
    to_dict,
)

from chain3.middleware import (
    http_retry_request_middleware,
)
from chain3.utils.datastructures import (
    NamedElementOnion,
)
from chain3.utils.http import (
    construct_user_agent,
)
from chain3.utils.request import (
    make_post_request,
)

from .base import (
    JSONBaseProvider,
)


def get_default_endpoint():
    return os.environ.get('chain3_HTTP_PROVIDER_URI', 'http://localhost:8545')


class HTTPProvider(JSONBaseProvider):
    logger = logging.getLogger("chain3.providers.HTTPProvider")
    endpoint_uri = None
    _request_args = None
    _request_kwargs = None
    _middlewares = NamedElementOnion([(http_retry_request_middleware, 'http_retry_request')])

    def __init__(self, endpoint_uri=None, request_kwargs=None):
        if endpoint_uri is None:
            self.endpoint_uri = get_default_endpoint()
        else:
            self.endpoint_uri = endpoint_uri
        self._request_kwargs = request_kwargs or {}
        super().__init__()

    def __str__(self):
        return "RPC connection {0}".format(self.endpoint_uri)

    @to_dict
    def get_request_kwargs(self):
        if 'headers' not in self._request_kwargs:
            yield 'headers', self.get_request_headers()
        for key, value in self._request_kwargs.items():
            yield key, value

    def get_request_headers(self):
        return {
            'Content-Type': 'application/json',
            'User-Agent': construct_user_agent(str(type(self))),
        }

    def make_request(self, method, params):
        self.logger.debug("Making request HTTP. URI: %s, Method: %s",
                          self.endpoint_uri, method)
        #print("Making request HTTP. URI: %s, Method: %s params %s", self.endpoint_uri, method, params)
        request_data = self.encode_rpc_request(method, params)
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        #print("Getting response HTTP. URI: %s, Method: %s, Response: %s", self.endpoint_uri, method, raw_response)
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Method: %s, Response: %s",
                          self.endpoint_uri, method, response)
        #print("Getting response HTTP. URI: %s, Method: %s, Response: %s", self.endpoint_uri, method, response)
        return response
