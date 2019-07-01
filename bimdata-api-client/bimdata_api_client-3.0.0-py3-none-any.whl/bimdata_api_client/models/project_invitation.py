# coding: utf-8

"""
    BIMData API

    BIMData API is a tool to interact with your models stored on BIMData’s servers.     Through the API, you can manage your projects, the clouds, upload your IFC files and manage them through endpoints.  # noqa: E501

    The version of the OpenAPI document: v1
    Contact: contact@bimdata.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ProjectInvitation(object):
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
        'id': 'int',
        'email': 'str',
        'redirect_uri': 'str',
        'role': 'int'
    }

    attribute_map = {
        'id': 'id',
        'email': 'email',
        'redirect_uri': 'redirect_uri',
        'role': 'role'
    }

    def __init__(self, id=None, email=None, redirect_uri=None, role=None):  # noqa: E501
        """ProjectInvitation - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._email = None
        self._redirect_uri = None
        self._role = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.email = email
        self.redirect_uri = redirect_uri
        self.role = role

    @property
    def id(self):
        """Gets the id of this ProjectInvitation.  # noqa: E501


        :return: The id of this ProjectInvitation.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ProjectInvitation.


        :param id: The id of this ProjectInvitation.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def email(self):
        """Gets the email of this ProjectInvitation.  # noqa: E501

        email of the user to invite  # noqa: E501

        :return: The email of this ProjectInvitation.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this ProjectInvitation.

        email of the user to invite  # noqa: E501

        :param email: The email of this ProjectInvitation.  # noqa: E501
        :type: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501
        if email is not None and len(email) > 256:
            raise ValueError("Invalid value for `email`, length must be less than or equal to `256`")  # noqa: E501
        if email is not None and len(email) < 1:
            raise ValueError("Invalid value for `email`, length must be greater than or equal to `1`")  # noqa: E501

        self._email = email

    @property
    def redirect_uri(self):
        """Gets the redirect_uri of this ProjectInvitation.  # noqa: E501

        User will be redirected to this uri when they accept the invitation  # noqa: E501

        :return: The redirect_uri of this ProjectInvitation.  # noqa: E501
        :rtype: str
        """
        return self._redirect_uri

    @redirect_uri.setter
    def redirect_uri(self, redirect_uri):
        """Sets the redirect_uri of this ProjectInvitation.

        User will be redirected to this uri when they accept the invitation  # noqa: E501

        :param redirect_uri: The redirect_uri of this ProjectInvitation.  # noqa: E501
        :type: str
        """
        if redirect_uri is None:
            raise ValueError("Invalid value for `redirect_uri`, must not be `None`")  # noqa: E501
        if redirect_uri is not None and len(redirect_uri) > 512:
            raise ValueError("Invalid value for `redirect_uri`, length must be less than or equal to `512`")  # noqa: E501
        if redirect_uri is not None and len(redirect_uri) < 1:
            raise ValueError("Invalid value for `redirect_uri`, length must be greater than or equal to `1`")  # noqa: E501

        self._redirect_uri = redirect_uri

    @property
    def role(self):
        """Gets the role of this ProjectInvitation.  # noqa: E501


        :return: The role of this ProjectInvitation.  # noqa: E501
        :rtype: int
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this ProjectInvitation.


        :param role: The role of this ProjectInvitation.  # noqa: E501
        :type: int
        """
        if role is None:
            raise ValueError("Invalid value for `role`, must not be `None`")  # noqa: E501

        self._role = role

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
        if not isinstance(other, ProjectInvitation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
