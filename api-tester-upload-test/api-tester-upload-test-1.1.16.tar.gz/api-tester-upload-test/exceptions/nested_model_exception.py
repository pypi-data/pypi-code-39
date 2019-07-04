# -*- coding: utf-8 -*-

"""
    api-tester-upload-test

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

from api-tester-upload-test.api_helper import APIHelper
import api-tester-upload-test.exceptions.api_exception
import api-tester-upload-test.models.validate

class NestedModelException(api-tester-upload-test.exceptions.api_exception.APIException):
    def __init__(self, reason, context):
        """Constructor for the NestedModelException class

        Args:
            reason (string): The reason (or error message) for the Exception
                to be raised.
            context (HttpContext):  The HttpContext of the API call.

        """
        super(NestedModelException, self).__init__(reason, context)
        dictionary = APIHelper.json_deserialize(self.context.response.raw_body)
        if isinstance(dictionary, dict):
            self.unbox(dictionary)

    def unbox(self, dictionary):
        """Populates the properties of this object by extracting them from a dictionary.

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        """
        self.server_message = dictionary.get('ServerMessage')
        self.server_code = dictionary.get('ServerCode')
        self.model = api-tester-upload-test.models.validate.Validate.from_dictionary(dictionary.get('model')) if dictionary.get('model') else None
