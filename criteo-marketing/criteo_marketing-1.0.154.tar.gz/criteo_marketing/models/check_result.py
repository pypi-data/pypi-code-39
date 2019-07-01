# coding: utf-8

"""
    Marketing API v.1.0

    IMPORTANT: This swagger links to Criteo production environment. Any test applied here will thus impact real campaigns.  # noqa: E501

    OpenAPI spec version: v.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class CheckResult(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'check_name': 'str',
        'successful': 'bool',
        'error': 'str',
        'inner_check_results': 'list[CheckResult]'
    }

    attribute_map = {
        'check_name': 'checkName',
        'successful': 'successful',
        'error': 'error',
        'inner_check_results': 'innerCheckResults'
    }

    def __init__(self, check_name=None, successful=None, error=None, inner_check_results=None):  # noqa: E501
        """CheckResult - a model defined in OpenAPI"""  # noqa: E501

        self._check_name = None
        self._successful = None
        self._error = None
        self._inner_check_results = None
        self.discriminator = None

        if check_name is not None:
            self.check_name = check_name
        if successful is not None:
            self.successful = successful
        if error is not None:
            self.error = error
        if inner_check_results is not None:
            self.inner_check_results = inner_check_results

    @property
    def check_name(self):
        """Gets the check_name of this CheckResult.  # noqa: E501


        :return: The check_name of this CheckResult.  # noqa: E501
        :rtype: str
        """
        return self._check_name

    @check_name.setter
    def check_name(self, check_name):
        """Sets the check_name of this CheckResult.


        :param check_name: The check_name of this CheckResult.  # noqa: E501
        :type: str
        """

        self._check_name = check_name

    @property
    def successful(self):
        """Gets the successful of this CheckResult.  # noqa: E501


        :return: The successful of this CheckResult.  # noqa: E501
        :rtype: bool
        """
        return self._successful

    @successful.setter
    def successful(self, successful):
        """Sets the successful of this CheckResult.


        :param successful: The successful of this CheckResult.  # noqa: E501
        :type: bool
        """

        self._successful = successful

    @property
    def error(self):
        """Gets the error of this CheckResult.  # noqa: E501


        :return: The error of this CheckResult.  # noqa: E501
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this CheckResult.


        :param error: The error of this CheckResult.  # noqa: E501
        :type: str
        """

        self._error = error

    @property
    def inner_check_results(self):
        """Gets the inner_check_results of this CheckResult.  # noqa: E501


        :return: The inner_check_results of this CheckResult.  # noqa: E501
        :rtype: list[CheckResult]
        """
        return self._inner_check_results

    @inner_check_results.setter
    def inner_check_results(self, inner_check_results):
        """Sets the inner_check_results of this CheckResult.


        :param inner_check_results: The inner_check_results of this CheckResult.  # noqa: E501
        :type: list[CheckResult]
        """

        self._inner_check_results = inner_check_results

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CheckResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
