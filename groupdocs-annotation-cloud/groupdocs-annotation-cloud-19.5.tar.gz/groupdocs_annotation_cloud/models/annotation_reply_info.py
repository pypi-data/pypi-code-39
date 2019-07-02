# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="AnnotationReplyInfo.py">
#   Copyright (c) 2003-2019 Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import pprint
import re  # noqa: F401

import six

class AnnotationReplyInfo(object):
    """
    Describes annotation reply properties
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'guid': 'str',
        'user_guid': 'str',
        'user_name': 'str',
        'user_email': 'str',
        'message': 'str',
        'replied_on': 'datetime',
        'parent_reply_guid': 'str'
    }

    attribute_map = {
        'guid': 'Guid',
        'user_guid': 'UserGuid',
        'user_name': 'UserName',
        'user_email': 'UserEmail',
        'message': 'Message',
        'replied_on': 'RepliedOn',
        'parent_reply_guid': 'ParentReplyGuid'
    }

    def __init__(self, guid=None, user_guid=None, user_name=None, user_email=None, message=None, replied_on=None, parent_reply_guid=None, **kwargs):  # noqa: E501
        """Initializes new instance of AnnotationReplyInfo"""  # noqa: E501

        self._guid = None
        self._user_guid = None
        self._user_name = None
        self._user_email = None
        self._message = None
        self._replied_on = None
        self._parent_reply_guid = None

        if guid is not None:
            self.guid = guid
        if user_guid is not None:
            self.user_guid = user_guid
        if user_name is not None:
            self.user_name = user_name
        if user_email is not None:
            self.user_email = user_email
        if message is not None:
            self.message = message
        if replied_on is not None:
            self.replied_on = replied_on
        if parent_reply_guid is not None:
            self.parent_reply_guid = parent_reply_guid
    
    @property
    def guid(self):
        """
        Gets the guid.  # noqa: E501

        Gets or sets the unique identifier  # noqa: E501

        :return: The guid.  # noqa: E501
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """
        Sets the guid.

        Gets or sets the unique identifier  # noqa: E501

        :param guid: The guid.  # noqa: E501
        :type: str
        """
        self._guid = guid
    
    @property
    def user_guid(self):
        """
        Gets the user_guid.  # noqa: E501

        Gets or sets the user's unique identifier  # noqa: E501

        :return: The user_guid.  # noqa: E501
        :rtype: str
        """
        return self._user_guid

    @user_guid.setter
    def user_guid(self, user_guid):
        """
        Sets the user_guid.

        Gets or sets the user's unique identifier  # noqa: E501

        :param user_guid: The user_guid.  # noqa: E501
        :type: str
        """
        self._user_guid = user_guid
    
    @property
    def user_name(self):
        """
        Gets the user_name.  # noqa: E501

        Gets or sets the user's name  # noqa: E501

        :return: The user_name.  # noqa: E501
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """
        Sets the user_name.

        Gets or sets the user's name  # noqa: E501

        :param user_name: The user_name.  # noqa: E501
        :type: str
        """
        self._user_name = user_name
    
    @property
    def user_email(self):
        """
        Gets the user_email.  # noqa: E501

        Gets or sets the user email  # noqa: E501

        :return: The user_email.  # noqa: E501
        :rtype: str
        """
        return self._user_email

    @user_email.setter
    def user_email(self, user_email):
        """
        Sets the user_email.

        Gets or sets the user email  # noqa: E501

        :param user_email: The user_email.  # noqa: E501
        :type: str
        """
        self._user_email = user_email
    
    @property
    def message(self):
        """
        Gets the message.  # noqa: E501

        Gets or sets the message  # noqa: E501

        :return: The message.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message.

        Gets or sets the message  # noqa: E501

        :param message: The message.  # noqa: E501
        :type: str
        """
        self._message = message
    
    @property
    def replied_on(self):
        """
        Gets the replied_on.  # noqa: E501

        Gets or sets the reply time  # noqa: E501

        :return: The replied_on.  # noqa: E501
        :rtype: datetime
        """
        return self._replied_on

    @replied_on.setter
    def replied_on(self, replied_on):
        """
        Sets the replied_on.

        Gets or sets the reply time  # noqa: E501

        :param replied_on: The replied_on.  # noqa: E501
        :type: datetime
        """
        if replied_on is None:
            raise ValueError("Invalid value for `replied_on`, must not be `None`")  # noqa: E501
        self._replied_on = replied_on
    
    @property
    def parent_reply_guid(self):
        """
        Gets the parent_reply_guid.  # noqa: E501

        Gets or sets the parent reply unique identifier  # noqa: E501

        :return: The parent_reply_guid.  # noqa: E501
        :rtype: str
        """
        return self._parent_reply_guid

    @parent_reply_guid.setter
    def parent_reply_guid(self, parent_reply_guid):
        """
        Sets the parent_reply_guid.

        Gets or sets the parent reply unique identifier  # noqa: E501

        :param parent_reply_guid: The parent_reply_guid.  # noqa: E501
        :type: str
        """
        self._parent_reply_guid = parent_reply_guid

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if not isinstance(other, AnnotationReplyInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
