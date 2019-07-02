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
import dateutil.parser
from tester.models.company import Company
from tester.models.company import BossCompany
from tester.models.company import EmployeeComp
from tester.models.company import Developer
from tester.models.company import SoftwareTester
from tester.models.complex_1 import Complex1
from tester.models.response_with_enum import ResponseWithEnum
from tester.models.complex_2 import Complex2
from tester.models.complex_3 import Complex3
from tester.models.person import Person


class ResponseTypesController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, config, call_back=None):
        super(ResponseTypesController, self).__init__(config, call_back)

    def get_date_array(self):
        """Does a GET request to /response/date.

        TODO: type endpoint description here.

        Returns:
            list of date: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/date'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = [dateutil.parser.parse(element).date() for element in APIHelper.json_deserialize(_response.raw_body)]

        return decoded

    def get_date(self):
        """Does a GET request to /response/date.

        TODO: type endpoint description here.

        Returns:
            date: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/date'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = dateutil.parser.parse(_response.raw_body).date()

        return decoded

    def return_company_model(self):
        """Does a GET request to /response/company.

        TODO: type endpoint description here.

        Returns:
            Company: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/company'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, Company.from_dictionary)

        return decoded

    def return_boss_model(self):
        """Does a GET request to /response/boss.

        TODO: type endpoint description here.

        Returns:
            BossCompany: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/boss'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, BossCompany.from_dictionary)

        return decoded

    def return_employee_model(self):
        """Does a GET request to /response/employee.

        TODO: type endpoint description here.

        Returns:
            EmployeeComp: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/employee'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, EmployeeComp.from_dictionary)

        return decoded

    def return_developer_model(self):
        """Does a GET request to /response/developer.

        TODO: type endpoint description here.

        Returns:
            Developer: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/developer'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, Developer.from_dictionary)

        return decoded

    def return_tester_model(self):
        """Does a GET request to /response/tester.

        TODO: type endpoint description here.

        Returns:
            SoftwareTester: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/tester'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, SoftwareTester.from_dictionary)

        return decoded

    def return_complex_1_object(self):
        """Does a GET request to /response/complex1.

        TODO: type endpoint description here.

        Returns:
            Complex1: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/complex1'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, Complex1.from_dictionary)

        return decoded

    def return_response_with_enums(self):
        """Does a GET request to /response/responseWitEnum.

        TODO: type endpoint description here.

        Returns:
            ResponseWithEnum: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/responseWitEnum'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, ResponseWithEnum.from_dictionary)

        return decoded

    def return_complex_2_object(self):
        """Does a GET request to /response/complex2.

        TODO: type endpoint description here.

        Returns:
            Complex2: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/complex2'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, Complex2.from_dictionary)

        return decoded

    def return_complex_3_object(self):
        """Does a GET request to /response/complex3.

        TODO: type endpoint description here.

        Returns:
            Complex3: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/complex3'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, Complex3.from_dictionary)

        return decoded

    def get_long(self):
        """Does a GET request to /response/long.

        TODO: type endpoint description here.

        Returns:
            long|int: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/long'
        _query_builder = self.config.get_base_uri(Server.DEFAULT)
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = int(_response.raw_body)

        return decoded

    def get_model(self):
        """Does a GET request to /response/model.

        TODO: type endpoint description here.

        Returns:
            Person: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/model'
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

        decoded = APIHelper.json_deserialize(_response.raw_body, Person.from_dictionary)

        return decoded

    def get_string_enum_array(self):
        """Does a GET request to /response/enum.

        TODO: type endpoint description here.

        Returns:
            list of Days: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/enum'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True,
            'type': 'string'
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_string_enum(self):
        """Does a GET request to /response/enum.

        TODO: type endpoint description here.

        Returns:
            Days: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/enum'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'type': 'string'
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = _response.raw_body

        return decoded

    def get_model_array(self):
        """Does a GET request to /response/model.

        TODO: type endpoint description here.

        Returns:
            list of Person: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/model'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = APIHelper.json_deserialize(_response.raw_body, Person.from_dictionary)

        return decoded

    def get_int_enum(self):
        """Does a GET request to /response/enum.

        TODO: type endpoint description here.

        Returns:
            SuiteCode: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/enum'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'type': 'int'
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = int(_response.raw_body)

        return decoded

    def get_int_enum_array(self):
        """Does a GET request to /response/enum.

        TODO: type endpoint description here.

        Returns:
            list of SuiteCode: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/enum'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True,
            'type': 'int'
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_precision(self):
        """Does a GET request to /response/precision.

        TODO: type endpoint description here.

        Returns:
            float: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/precision'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = float(_response.raw_body)

        return decoded

    def get_binary(self):
        """Does a GET request to /response/binary.

        gets a binary object

        Returns:
            binary: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/binary'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request, binary=True)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = _response.raw_body

        return decoded

    def get_integer(self):
        """Does a GET request to /response/integer.

        Gets a integer response

        Returns:
            int: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/integer'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = int(_response.raw_body)

        return decoded

    def get_integer_array(self):
        """Does a GET request to /response/integer.

        Get an array of integers.

        Returns:
            list of int: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/integer'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_dynamic(self):
        """Does a GET request to /response/dynamic.

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
        _url_path = '/response/dynamic'
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

    def get_dynamic_array(self):
        """Does a GET request to /response/dynamic.

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
        _url_path = '/response/dynamic'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

    def get_3339_datetime(self):
        """Does a GET request to /response/3339datetime.

        TODO: type endpoint description here.

        Returns:
            datetime: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/3339datetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = APIHelper.RFC3339DateTime.from_value(_response.raw_body).datetime

        return decoded

    def get_3339_datetime_array(self):
        """Does a GET request to /response/3339datetime.

        TODO: type endpoint description here.

        Returns:
            list of datetime: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/3339datetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = [element.datetime for element in APIHelper.json_deserialize(_response.raw_body, APIHelper.RFC3339DateTime.from_value)]

        return decoded

    def get_boolean(self):
        """Does a GET request to /response/boolean.

        TODO: type endpoint description here.

        Returns:
            bool: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/boolean'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = _response.raw_body == 'true'

        return decoded

    def get_boolean_array(self):
        """Does a GET request to /response/boolean.

        TODO: type endpoint description here.

        Returns:
            list of bool: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/boolean'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = APIHelper.json_deserialize(_response.raw_body)

        return decoded

    def get_headers(self):
        """Does a GET request to /response/headers.

        TODO: type endpoint description here.

        Returns:
            void: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/headers'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)
        self.validate_response(_response)

    def get_1123_date_time(self):
        """Does a GET request to /response/1123datetime.

        TODO: type endpoint description here.

        Returns:
            datetime: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/1123datetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = APIHelper.HttpDateTime.from_value(_response.raw_body).datetime

        return decoded

    def get_unix_date_time(self):
        """Does a GET request to /response/unixdatetime.

        TODO: type endpoint description here.

        Returns:
            datetime: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/unixdatetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _response.status_code == 404:
            return None
        self.validate_response(_response)

        decoded = APIHelper.UnixDateTime.from_value(_response.raw_body).datetime

        return decoded

    def get_1123_date_time_array(self):
        """Does a GET request to /response/1123datetime.

        TODO: type endpoint description here.

        Returns:
            list of datetime: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/1123datetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = [element.datetime for element in APIHelper.json_deserialize(_response.raw_body, APIHelper.HttpDateTime.from_value)]

        return decoded

    def get_unix_date_time_array(self):
        """Does a GET request to /response/unixdatetime.

        TODO: type endpoint description here.

        Returns:
            list of datetime: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/unixdatetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters
        )
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

        decoded = [element.datetime for element in APIHelper.json_deserialize(_response.raw_body, APIHelper.UnixDateTime.from_value)]

        return decoded

    def get_content_type_headers(self):
        """Does a GET request to /response/getContentType.

        TODO: type endpoint description here.

        Returns:
            void: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/response/getContentType'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url)
        _response = self.execute_request(_request)
        self.validate_response(_response)
