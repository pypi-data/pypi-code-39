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


class SellerCampaignMessage(object):
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
        'id': 'str',
        'seller_id': 'str',
        'campaign_id': 'int',
        'bid': 'float',
        'suspended_since': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'seller_id': 'sellerId',
        'campaign_id': 'campaignId',
        'bid': 'bid',
        'suspended_since': 'suspendedSince'
    }

    def __init__(self, id=None, seller_id=None, campaign_id=None, bid=None, suspended_since=None):  # noqa: E501
        """SellerCampaignMessage - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._seller_id = None
        self._campaign_id = None
        self._bid = None
        self._suspended_since = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if seller_id is not None:
            self.seller_id = seller_id
        if campaign_id is not None:
            self.campaign_id = campaign_id
        if bid is not None:
            self.bid = bid
        if suspended_since is not None:
            self.suspended_since = suspended_since

    @property
    def id(self):
        """Gets the id of this SellerCampaignMessage.  # noqa: E501


        :return: The id of this SellerCampaignMessage.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SellerCampaignMessage.


        :param id: The id of this SellerCampaignMessage.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def seller_id(self):
        """Gets the seller_id of this SellerCampaignMessage.  # noqa: E501


        :return: The seller_id of this SellerCampaignMessage.  # noqa: E501
        :rtype: str
        """
        return self._seller_id

    @seller_id.setter
    def seller_id(self, seller_id):
        """Sets the seller_id of this SellerCampaignMessage.


        :param seller_id: The seller_id of this SellerCampaignMessage.  # noqa: E501
        :type: str
        """

        self._seller_id = seller_id

    @property
    def campaign_id(self):
        """Gets the campaign_id of this SellerCampaignMessage.  # noqa: E501


        :return: The campaign_id of this SellerCampaignMessage.  # noqa: E501
        :rtype: int
        """
        return self._campaign_id

    @campaign_id.setter
    def campaign_id(self, campaign_id):
        """Sets the campaign_id of this SellerCampaignMessage.


        :param campaign_id: The campaign_id of this SellerCampaignMessage.  # noqa: E501
        :type: int
        """

        self._campaign_id = campaign_id

    @property
    def bid(self):
        """Gets the bid of this SellerCampaignMessage.  # noqa: E501


        :return: The bid of this SellerCampaignMessage.  # noqa: E501
        :rtype: float
        """
        return self._bid

    @bid.setter
    def bid(self, bid):
        """Sets the bid of this SellerCampaignMessage.


        :param bid: The bid of this SellerCampaignMessage.  # noqa: E501
        :type: float
        """

        self._bid = bid

    @property
    def suspended_since(self):
        """Gets the suspended_since of this SellerCampaignMessage.  # noqa: E501


        :return: The suspended_since of this SellerCampaignMessage.  # noqa: E501
        :rtype: datetime
        """
        return self._suspended_since

    @suspended_since.setter
    def suspended_since(self, suspended_since):
        """Sets the suspended_since of this SellerCampaignMessage.


        :param suspended_since: The suspended_since of this SellerCampaignMessage.  # noqa: E501
        :type: datetime
        """

        self._suspended_since = suspended_since

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
        if not isinstance(other, SellerCampaignMessage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
