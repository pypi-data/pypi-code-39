# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""

from tester.api_helper import APIHelper
from tester.configuration import Configuration
from tester.configuration import Server
from tester.controllers.base_controller import BaseController
from tester.models.complex_5 import Complex5
from tester.exceptions.nested_model_exception import NestedModelException
from tester.exceptions.local_test_exception import LocalTestException
from tester.exceptions.unix_time_stamp_exception import UnixTimeStampException
from tester.exceptions.rfc_1123_exception import Rfc1123Exception
from tester.exceptions.exception_with_rfc_3339_date_time_exception import ExceptionWithRfc3339DateTimeException
from tester.exceptions.custom_error_response_exception import CustomErrorResponseException
from tester.exceptions.exception_with_date_exception import ExceptionWithDateException
from tester.exceptions.exception_with_uuid_exception import ExceptionWithUUIDException
from tester.exceptions.exception_with_dynamic_exception import ExceptionWithDynamicException
from tester.exceptions.exception_with_precision_exception import ExceptionWithPrecisionException
from tester.exceptions.exception_with_boolean_exception import ExceptionWithBooleanException
from tester.exceptions.exception_with_long_exception import ExceptionWithLongException
from tester.exceptions.exception_with_number_exception import ExceptionWithNumberException
from tester.exceptions.exception_with_string_exception import ExceptionWithStringException


class ErrorCodesController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, config, call_back=None):
        super(ErrorCodesController, self).__init__(config, call_back)

    def catch_412_global_error(self):
        """Does a GET request to /error/412.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/412'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_501(self):
        """Does a GET request to /error/501.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/501'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 501:
            raise NestedModelException('error 501', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_400(self):
        """Does a GET request to /error/400.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/400'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_500(self):
        """Does a GET request to /error/500.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/500'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_401(self):
        """Does a GET request to /error/401.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/401'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 401:
            raise LocalTestException('401 Local', _response)
        elif _response.status_code == 421:
            raise LocalTestException('Default', _response)
        elif _response.status_code == 431:
            raise LocalTestException('Default', _response)
        elif _response.status_code == 432:
            raise LocalTestException('Default', _response)
        elif _response.status_code == 441:
            raise LocalTestException('Default', _response)
        elif (_response.status_code < 200) or (_response.status_code > 208):
            raise LocalTestException('Invalid response.', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def receive_exception_with_unixtimestamp_exception(self):
        """Does a GET request to /error/unixTimeStampException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/unixTimeStampException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise UnixTimeStampException('unixtimestamp exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def receive_exception_with_rfc_1123_datetime(self):
        """Does a GET request to /error/rfc1123Exception.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/rfc1123Exception'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise Rfc1123Exception('Rfc1123 Exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def receive_exception_with_rfc_3339_datetime(self):
        """Does a GET request to /error/Rfc3339InException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/Rfc3339InException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithRfc3339DateTimeException('DateTime Exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def receive_endpoint_level_exception(self):
        """Does a GET request to /error/451.

        TODO: type endpoint description here.

        Returns:
            Complex5: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/451'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 451:
            raise CustomErrorResponseException('caught endpoint exception', _response)
        self.validate_response(_response)

        decoded = APIHelper.json_deserialize(_response.raw_body, Complex5.from_dictionary)

        return decoded

    def receive_global_level_exception(self):
        """Does a GET request to /error/450.

        TODO: type endpoint description here.

        Returns:
            Complex5: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/450'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = APIHelper.json_deserialize(_response.raw_body, Complex5.from_dictionary)

        return decoded

    def date_in_exception(self):
        """Does a GET request to /error/dateInException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/dateInException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithDateException('date in exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def uuid_in_exception(self):
        """Does a GET request to /error/uuidInException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/uuidInException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithUUIDException('uuid in exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def dynamic_in_exception(self):
        """Does a GET request to /error/dynamicInException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/dynamicInException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithDynamicException('dynamic in Exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def precision_in_exception(self):
        """Does a GET request to /error/precisionInException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/precisionInException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithPrecisionException('precision in Exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def boolean_in_exception(self):
        """Does a GET request to /error/booleanInException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/booleanInException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithBooleanException('Boolean in Exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def long_in_exception(self):
        """Does a GET request to /error/longInException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/longInException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithLongException('long in exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def number_in_exception(self):
        """Does a GET request to /error/numberInException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/numberInException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithNumberException('number in exception', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_exception_with_string(self):
        """Does a GET request to /error/stringInException.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/error/stringInException'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        elif _response.status_code == 444:
            raise ExceptionWithStringException('exception with string', _response)
        self.validate_response(_response)
        if (_response.raw_body is not None) or (not str(_response.raw_body)):
            decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded
