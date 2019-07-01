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


class MessageWithDetailsCampaignBidChangeResponse(object):
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
        'message': 'str',
        'details': 'CampaignBidChangeResponse'
    }

    attribute_map = {
        'message': 'message',
        'details': 'details'
    }

    def __init__(self, message=None, details=None):  # noqa: E501
        """MessageWithDetailsCampaignBidChangeResponse - a model defined in OpenAPI"""  # noqa: E501

        self._message = None
        self._details = None
        self.discriminator = None

        if message is not None:
            self.message = message
        if details is not None:
            self.details = details

    @property
    def message(self):
        """Gets the message of this MessageWithDetailsCampaignBidChangeResponse.  # noqa: E501


        :return: The message of this MessageWithDetailsCampaignBidChangeResponse.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this MessageWithDetailsCampaignBidChangeResponse.


        :param message: The message of this MessageWithDetailsCampaignBidChangeResponse.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def details(self):
        """Gets the details of this MessageWithDetailsCampaignBidChangeResponse.  # noqa: E501


        :return: The details of this MessageWithDetailsCampaignBidChangeResponse.  # noqa: E501
        :rtype: CampaignBidChangeResponse
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this MessageWithDetailsCampaignBidChangeResponse.


        :param details: The details of this MessageWithDetailsCampaignBidChangeResponse.  # noqa: E501
        :type: CampaignBidChangeResponse
        """

        self._details = details

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
        if not isinstance(other, MessageWithDetailsCampaignBidChangeResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
