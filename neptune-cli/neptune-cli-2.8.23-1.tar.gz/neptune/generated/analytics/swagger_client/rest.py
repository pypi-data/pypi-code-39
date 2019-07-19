# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Credit: this file (rest.py) is modified based on rest.py in Dropbox Python SDK:
https://www.dropbox.com/developers/core/sdks/python
"""
from __future__ import absolute_import

import sys
import io
import json
import ssl
import certifi
import logging

# python 2 and python 3 compatibility library
from six import iteritems

from .configuration import Configuration

try:
    import requests
    import requests_oauthlib
except ImportError:
    raise ImportError('Swagger python client requires requests and requests_oauthlib.')

try:
    # for python3
    from urllib.parse import urlencode
except ImportError:
    # for python2
    from urllib import urlencode


logger = logging.getLogger(__name__)


class RESTResponse(io.IOBase):

    def __init__(self, resp):
        self.requests_response = resp
        self.status = resp.status_code
        self.reason = resp.reason
        self.data = resp.text

    def getheaders(self):
        """
        Returns a dictionary of the response headers.
        """
        return self.requests_response.headers

    def getheader(self, name, default=None):
        """
        Returns a given response header.
        """
        return self.getheaders().get(name, default)


class RESTClientObject(object):

    def __init__(self, requests_client, timeout=None):
        self.requests_client = requests_client
        self.timeout = timeout

    def request(self, method, url, query_params=None, headers=None,
                body=None, post_params=None):
        """
        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencode`
                            and `multipart/form-data`
        """
        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS']

        if post_params and body:
            raise ValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        try:
            if query_params:
                url += '?' + urlencode(self._encode_unicode_characters(query_params), True)
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
                if headers['Content-Type'] == 'application/json':
                    r = self.requests_client.request(method, url, json=body, headers=headers, timeout=self.timeout)
                if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                    r = self.requests_client.request(method, url, data=post_params, headers=headers, timeout=self.timeout)
                if headers['Content-Type'] == 'application/octet-stream':
                    r = self.requests_client.request(method, url, data=post_params, headers=headers, timeout=self.timeout)
                if headers['Content-Type'] == 'multipart/form-data':
                    del headers['Content-Type']
                    r = self.requests_client.request(method, url, files=post_params, headers=headers, timeout=self.timeout)
            # For `GET`, `HEAD`
            else:
                r = self.requests_client.request(method, url, headers=headers, timeout=self.timeout)
        except requests.exceptions.SSLError as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise ApiException(status=0, reason=msg)

        r = RESTResponse(r)

        # log response body
        logger.debug("response body: %s" % r.data)

        if r.status not in range(200, 206):
            raise ApiException(http_resp=r)

        return r

    def GET(self, url, headers=None, query_params=None):
        return self.request("GET", url,
                            headers=headers,
                            query_params=query_params)

    def HEAD(self, url, headers=None, query_params=None):
        return self.request("HEAD", url,
                            headers=headers,
                            query_params=query_params)

    def OPTIONS(self, url, headers=None, query_params=None, post_params=None, body=None):
        return self.request("OPTIONS", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            body=body)

    def DELETE(self, url, headers=None, query_params=None, body=None):
        return self.request("DELETE", url,
                            headers=headers,
                            query_params=query_params,
                            body=body)

    def POST(self, url, headers=None, query_params=None, post_params=None, body=None):
        return self.request("POST", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            body=body)

    def PUT(self, url, headers=None, query_params=None, post_params=None, body=None):
        return self.request("PUT", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            body=body)

    def PATCH(self, url, headers=None, query_params=None, post_params=None, body=None):
        return self.request("PATCH", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            body=body)

    def _encode_unicode_characters(self, obj):
        if type(obj) is list:
            return [self._encode_unicode_characters(el) for el in obj]
        elif type(obj) is tuple:
            return tuple(self._encode_unicode_characters(el) for el in obj)
        elif type(obj) is str:
            return obj.encode('utf-8')
        elif type(obj) is dict:
            return {
                self._encode_unicode_characters(key): self._encode_unicode_characters(value)
                for key, value in obj.items()
            }
        else:
            return str(obj)


class ApiException(Exception):

    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.body = http_resp.data
            self.headers = http_resp.getheaders()
            self.url = http_resp.requests_response.url
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None
            self.url = None

    def __str__(self):
        """
        Custom error messages for exception
        """
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message
