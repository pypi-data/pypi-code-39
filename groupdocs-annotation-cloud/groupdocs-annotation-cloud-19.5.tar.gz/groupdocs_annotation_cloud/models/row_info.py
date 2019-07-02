# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="RowInfo.py">
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

class RowInfo(object):
    """
    Describes text row information
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'character_coordinates': 'list[float]',
        'line_height': 'float',
        'line_left': 'float',
        'line_top': 'float',
        'line_width': 'float',
        'text': 'str',
        'text_coordinates': 'list[float]'
    }

    attribute_map = {
        'character_coordinates': 'CharacterCoordinates',
        'line_height': 'LineHeight',
        'line_left': 'LineLeft',
        'line_top': 'LineTop',
        'line_width': 'LineWidth',
        'text': 'Text',
        'text_coordinates': 'TextCoordinates'
    }

    def __init__(self, character_coordinates=None, line_height=None, line_left=None, line_top=None, line_width=None, text=None, text_coordinates=None, **kwargs):  # noqa: E501
        """Initializes new instance of RowInfo"""  # noqa: E501

        self._character_coordinates = None
        self._line_height = None
        self._line_left = None
        self._line_top = None
        self._line_width = None
        self._text = None
        self._text_coordinates = None

        if character_coordinates is not None:
            self.character_coordinates = character_coordinates
        if line_height is not None:
            self.line_height = line_height
        if line_left is not None:
            self.line_left = line_left
        if line_top is not None:
            self.line_top = line_top
        if line_width is not None:
            self.line_width = line_width
        if text is not None:
            self.text = text
        if text_coordinates is not None:
            self.text_coordinates = text_coordinates
    
    @property
    def character_coordinates(self):
        """
        Gets the character_coordinates.  # noqa: E501

        Gets or sets the list of character coordinates  # noqa: E501

        :return: The character_coordinates.  # noqa: E501
        :rtype: list[float]
        """
        return self._character_coordinates

    @character_coordinates.setter
    def character_coordinates(self, character_coordinates):
        """
        Sets the character_coordinates.

        Gets or sets the list of character coordinates  # noqa: E501

        :param character_coordinates: The character_coordinates.  # noqa: E501
        :type: list[float]
        """
        self._character_coordinates = character_coordinates
    
    @property
    def line_height(self):
        """
        Gets the line_height.  # noqa: E501

        Gets or sets the text line height  # noqa: E501

        :return: The line_height.  # noqa: E501
        :rtype: float
        """
        return self._line_height

    @line_height.setter
    def line_height(self, line_height):
        """
        Sets the line_height.

        Gets or sets the text line height  # noqa: E501

        :param line_height: The line_height.  # noqa: E501
        :type: float
        """
        if line_height is None:
            raise ValueError("Invalid value for `line_height`, must not be `None`")  # noqa: E501
        self._line_height = line_height
    
    @property
    def line_left(self):
        """
        Gets the line_left.  # noqa: E501

        Gets or sets the x coordinate of the text line upper left corner  # noqa: E501

        :return: The line_left.  # noqa: E501
        :rtype: float
        """
        return self._line_left

    @line_left.setter
    def line_left(self, line_left):
        """
        Sets the line_left.

        Gets or sets the x coordinate of the text line upper left corner  # noqa: E501

        :param line_left: The line_left.  # noqa: E501
        :type: float
        """
        if line_left is None:
            raise ValueError("Invalid value for `line_left`, must not be `None`")  # noqa: E501
        self._line_left = line_left
    
    @property
    def line_top(self):
        """
        Gets the line_top.  # noqa: E501

        Gets or sets the y coordinate of the text line upper left corner  # noqa: E501

        :return: The line_top.  # noqa: E501
        :rtype: float
        """
        return self._line_top

    @line_top.setter
    def line_top(self, line_top):
        """
        Sets the line_top.

        Gets or sets the y coordinate of the text line upper left corner  # noqa: E501

        :param line_top: The line_top.  # noqa: E501
        :type: float
        """
        if line_top is None:
            raise ValueError("Invalid value for `line_top`, must not be `None`")  # noqa: E501
        self._line_top = line_top
    
    @property
    def line_width(self):
        """
        Gets the line_width.  # noqa: E501

        Gets or sets the text line width  # noqa: E501

        :return: The line_width.  # noqa: E501
        :rtype: float
        """
        return self._line_width

    @line_width.setter
    def line_width(self, line_width):
        """
        Sets the line_width.

        Gets or sets the text line width  # noqa: E501

        :param line_width: The line_width.  # noqa: E501
        :type: float
        """
        if line_width is None:
            raise ValueError("Invalid value for `line_width`, must not be `None`")  # noqa: E501
        self._line_width = line_width
    
    @property
    def text(self):
        """
        Gets the text.  # noqa: E501

        Gets or sets the text  # noqa: E501

        :return: The text.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text.

        Gets or sets the text  # noqa: E501

        :param text: The text.  # noqa: E501
        :type: str
        """
        self._text = text
    
    @property
    def text_coordinates(self):
        """
        Gets the text_coordinates.  # noqa: E501

        Gets or sets the list of text coordinates  # noqa: E501

        :return: The text_coordinates.  # noqa: E501
        :rtype: list[float]
        """
        return self._text_coordinates

    @text_coordinates.setter
    def text_coordinates(self, text_coordinates):
        """
        Sets the text_coordinates.

        Gets or sets the list of text coordinates  # noqa: E501

        :param text_coordinates: The text_coordinates.  # noqa: E501
        :type: list[float]
        """
        self._text_coordinates = text_coordinates

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
        if not isinstance(other, RowInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
