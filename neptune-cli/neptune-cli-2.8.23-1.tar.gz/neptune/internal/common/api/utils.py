# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import logging
import time
from functools import wraps

from enum import Enum
from future.utils import raise_from, iteritems
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

from neptune.generated.swagger_client.rest import ApiException
from neptune.internal.common.api.exceptions import (
    NeptuneEntityNotFoundException,
    NeptuneServerRequestFailedException,
    NeptuneServerResponseErrorException,
    NeptuneRefreshTokenExpiredException,
    NeptuneUnprocessableEntityException,
    NeptuneBadClientRequest,
    ServerTimedOutException,
    NeptuneValidationException, NeptunePaymentRequiredException)
from neptune.internal.common.utils.time import compute_delay

logger = logging.getLogger(__name__)

ERROR_CODES_TO_RETRY = [0, 408, 500, 502, 503, 504]
MAX_RETRY_DELAY = 128
REQUESTS_TIMEOUT = 13


class APIErrorCodes(int, Enum):
    OK = 200
    MOVED = 302
    CLIENT_ERROR = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    TIMEOUT = 408
    PRECONDITION_FAILED = 412
    UNPROCESSABLE_ENTITY = 422


def swagger_model_to_json(model):
    """
    For Python, Swagger model properties are written in underscore_case. Model has to_dict() method,
    which converts the properties to JSON directly, preserving the underscore_case.
    The server expects camelCased properties. The mapping between different conventions is stored
    in Model.attribute_map property, but there is no method in the model to perform the conversion.
    :param model: Swagger model.
    :return: The model converted to JSON with renamed parameters, ready to be sent in a request.
    """
    result = {}

    for attr, _ in iteritems(model.swagger_types):
        value = getattr(model, attr)
        json_attr_name = model.attribute_map[attr]
        if isinstance(value, list):
            result[json_attr_name] = [
                swagger_model_to_json(x)
                if hasattr(x, "to_dict") else x for x in value]
        elif hasattr(value, "to_dict"):
            result[json_attr_name] = swagger_model_to_json(value)
        elif isinstance(value, dict):
            result[json_attr_name] = dict([
                (item[0], swagger_model_to_json(item[1]))
                if hasattr(item[1], "to_dict") else item for item in iteritems(value)])
        else:
            result[json_attr_name] = value

    return result


def retry_request(fun):
    def retry_loop(*args, **kwargs):
        attempt = 1
        while True:
            try:
                if attempt > 1:
                    logger.info(u"Request failed. Retrying...")
                result = fun(*args, **kwargs)
                if attempt > 1:
                    logger.info(u"Request succeeded!")
                return result
            except NeptuneServerResponseErrorException as response_error:
                if response_error.status not in ERROR_CODES_TO_RETRY:
                    logger.info(response_error)
                    raise response_error
                logger.debug(response_error)
            except NeptuneRefreshTokenExpiredException as exc:
                logger.debug(exc)
                raise exc
            except NeptuneServerRequestFailedException as exc:
                logger.debug(exc)

            delay = compute_delay(attempt, MAX_RETRY_DELAY)
            logger.info("Attempt #%d to call %s failed. Next try in %ds.",
                        attempt, fun.__name__, delay)
            time.sleep(delay)
            attempt += 1
    return retry_loop


def log_exceptions(skip_error_codes):
    def wrap(func):
        def func_wrapper(*args, **kwargs):
            func_wrapper.__name__ = func.__name__

            def log_exception(exc):
                logger.error('Failed to call ' + func.__name__)
                logger.exception(exc)

            try:
                return func(*args, **kwargs)
            except (NeptuneEntityNotFoundException, NeptuneValidationException, NeptuneBadClientRequest,
                    ServerTimedOutException, NeptuneRefreshTokenExpiredException, NeptuneServerRequestFailedException,
                    NeptunePaymentRequiredException):
                raise
            except NeptuneServerResponseErrorException as exc:
                if exc.status not in skip_error_codes:
                    log_exception(exc)
                raise
            except Exception as exc:
                log_exception(exc)
                raise
        return func_wrapper
    return wrap


def wrap_exceptions(func):
    """
    Wraps service exceptions as NeptuneException.
    In case of ApiException(302) from proxy - which means login page redirect,
    exception is mapped to ApiException(401) - unauthorized.
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except ApiException as exc:
            if exc.status == APIErrorCodes.PAYMENT_REQUIRED:
                raise NeptunePaymentRequiredException(exc.status, exc)
            elif exc.status == APIErrorCodes.NOT_FOUND:
                raise NeptuneEntityNotFoundException(exc.status, exc)
            elif exc.status == APIErrorCodes.UNPROCESSABLE_ENTITY:
                raise NeptuneUnprocessableEntityException(exc.status, exc)
            elif exc.status == APIErrorCodes.CLIENT_ERROR:
                if u'validationError' in exc.body:
                    raise NeptuneValidationException(exc)
                else:
                    raise NeptuneBadClientRequest(exc.status, exc)
            elif exc.status == APIErrorCodes.TIMEOUT:
                raise ServerTimedOutException(exc.status, exc)
            else:
                raise NeptuneServerResponseErrorException(exc.status, exc)
        except InvalidGrantError as err:
            logger.debug(err)
            if err.description == u'Stale refresh token':
                raise NeptuneRefreshTokenExpiredException()
            elif err.description == u'Client session not active':
                raise NeptuneRefreshTokenExpiredException()
            else:
                raise_from(NeptuneServerRequestFailedException(err), err)
        except Exception as exc:
            raise_from(NeptuneServerRequestFailedException(exc), exc)
    return func_wrapper


def handle_warning(func):
    def headers_handler(headers):
        if u'Warning' in headers:
            print(headers.get(u"Warning").replace(u"299 -", u"WARNING:"))

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        return func(*args, **dict(kwargs, headers_handler=headers_handler))

    return func_wrapper


class WithLoggedExceptions(object):
    CODES_SKIPPED_BY_DEFAULT = [APIErrorCodes.FORBIDDEN, APIErrorCodes.UNAUTHORIZED,
                                APIErrorCodes.UNPROCESSABLE_ENTITY, APIErrorCodes.CLIENT_ERROR]

    def __init__(self, obj, skipped_error_codes=None):
        self._obj = obj
        self._skipped_error_codes = skipped_error_codes or {}

    def __getattr__(self, name):

        method = getattr(self._obj, name)

        error_codes = self.CODES_SKIPPED_BY_DEFAULT
        if name in self._skipped_error_codes:
            error_codes = error_codes + self._skipped_error_codes[name]

        return log_exceptions(skip_error_codes=error_codes)(method)


class WithRetries(object):

    def __init__(self, obj, omit=None):
        self._obj = obj
        self._omitted = omit or []

    def __getattr__(self, name):

        method = getattr(self._obj, name)

        if name in self._omitted:
            return method
        else:
            return retry_request(method)


class WithWrappedExceptions(object):

    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        method = getattr(self._obj, name)
        return wrap_exceptions(method)


class WithWarningHandler(object):

    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        method = getattr(self._obj, name)
        return handle_warning(method)
