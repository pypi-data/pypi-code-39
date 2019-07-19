#
# Copyright (c) 2016, deepsense.io
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
import json

from future.builtins import str
from future.utils import python_2_unicode_compatible

from neptune.internal.common import NeptuneException, NeptuneInternalException


class NeptuneConnectionFailedException(NeptuneException):
    def __init__(self, http_url):
        super(NeptuneConnectionFailedException, self).__init__(
            str(u'Connection to Neptune Server ({}) failed.').format(http_url))


class InvalidApiVersionException(NeptuneException):
    def __init__(self, client_version, backend_version):
        super(InvalidApiVersionException, self).__init__(
            str(u'Version of the client library is '
                u'incompatible with version of Neptune Server!\n'
                u'Client version: {}, Server version: {}.').format(client_version, backend_version))


class NeptuneServerRequestFailedException(NeptuneInternalException):
    def __init__(self, cause):
        super(NeptuneServerRequestFailedException, self).__init__(
            str(u'Neptune server request failed: {}'.format(str(cause))))


class NeptuneRefreshTokenExpiredException(NeptuneException):
    def __init__(self):
        super(NeptuneRefreshTokenExpiredException, self).__init__(
            str(u'Stale refresh token. Please login again.'))


@python_2_unicode_compatible
class NeptuneServerResponseErrorException(NeptuneInternalException):
    def __init__(self, status, exc):
        self.url = exc.url
        self.status = status
        self.body = exc.body or str(exc)
        response_message = self._extract_exception_message(self.body)
        self.response_message = response_message
        exception_message = str(u'Neptune server response error! ({0}) {1}').format(
            status, response_message)
        super(NeptuneServerResponseErrorException, self).__init__(exception_message)

    @staticmethod
    def _extract_exception_message(response_body):
        try:
            return json.loads(response_body)['message']
        except (ValueError, KeyError):
            return response_body

    def __str__(self):
        return u"status: {}, response_message: {}".format(self.status, self.response_message)


class ServerTimedOutException(NeptuneServerResponseErrorException):
    def __str__(self):
        return u"Server timed out."


class NeptunePaymentRequiredException(NeptuneServerResponseErrorException):
    pass


class NeptuneEntityNotFoundException(NeptuneServerResponseErrorException):
    pass


class NeptuneUnprocessableEntityException(NeptuneServerResponseErrorException):
    pass


class NeptuneBadClientRequest(NeptuneServerResponseErrorException):
    pass


class NeptuneValidationException(NeptuneInternalException):
    def __init__(self, exc):
        exc_json = json.loads(exc.body)
        invalid_field_errors = [InvalidFieldError(error['path'], [FieldError(e) for e in error['errors']])
                                for error in exc_json['validationErrors']]
        self.validation_error = ValidationError(error_type=exc_json['errorType'],
                                                title=exc_json['title'],
                                                validation_errors=invalid_field_errors)
        super(NeptuneValidationException, self).__init__(str(self.validation_error))


class FieldError(object):
    def __init__(self, error_code=None, context=None):
        self._error_code = error_code
        self._context = context

    @property
    def error_code(self):
        return self._error_code

    @property
    def context(self):
        return self._context


class InvalidFieldError(object):
    def __init__(self, path=None, errors=None):
        self._path = path
        self._errors = errors

    @property
    def path(self):
        return self._path

    @property
    def errors(self):
        return self._errors


class ValidationError(object):
    def __init__(self, error_type=None, title=None, validation_errors=None):
        self._error_type = error_type
        self._title = title
        self._validation_errors = validation_errors

    @property
    def error_type(self):
        return self._error_type

    @property
    def title(self):
        return self._title

    @property
    def validation_errors(self):
        return self._validation_errors
