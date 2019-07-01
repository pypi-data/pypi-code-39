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


class LoyatyPoints(object):
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
        'name': 'str',
        'points_value': 'int',
        'ratio': 'float'
    }

    attribute_map = {
        'name': 'name',
        'points_value': 'pointsValue',
        'ratio': 'ratio'
    }

    def __init__(self, name=None, points_value=None, ratio=None):  # noqa: E501
        """LoyatyPoints - a model defined in OpenAPI"""  # noqa: E501

        self._name = None
        self._points_value = None
        self._ratio = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if points_value is not None:
            self.points_value = points_value
        if ratio is not None:
            self.ratio = ratio

    @property
    def name(self):
        """Gets the name of this LoyatyPoints.  # noqa: E501


        :return: The name of this LoyatyPoints.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LoyatyPoints.


        :param name: The name of this LoyatyPoints.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def points_value(self):
        """Gets the points_value of this LoyatyPoints.  # noqa: E501


        :return: The points_value of this LoyatyPoints.  # noqa: E501
        :rtype: int
        """
        return self._points_value

    @points_value.setter
    def points_value(self, points_value):
        """Sets the points_value of this LoyatyPoints.


        :param points_value: The points_value of this LoyatyPoints.  # noqa: E501
        :type: int
        """

        self._points_value = points_value

    @property
    def ratio(self):
        """Gets the ratio of this LoyatyPoints.  # noqa: E501


        :return: The ratio of this LoyatyPoints.  # noqa: E501
        :rtype: float
        """
        return self._ratio

    @ratio.setter
    def ratio(self, ratio):
        """Sets the ratio of this LoyatyPoints.


        :param ratio: The ratio of this LoyatyPoints.  # noqa: E501
        :type: float
        """

        self._ratio = ratio

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
        if not isinstance(other, LoyatyPoints):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
