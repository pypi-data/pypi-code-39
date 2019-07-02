# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="AnnotationInfo.py">
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

class AnnotationInfo(object):
    """
    Describes annotation properties
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
        'document_guid': 'int',
        'text': 'str',
        'creator_guid': 'str',
        'creator_name': 'str',
        'creator_email': 'str',
        'box': 'Rectangle',
        'page_number': 'int',
        'annotation_position': 'Point',
        'svg_path': 'str',
        'type': 'str',
        'access': 'str',
        'replies': 'list[AnnotationReplyInfo]',
        'created_on': 'datetime',
        'font_color': 'int',
        'pen_color': 'int',
        'pen_width': 'int',
        'pen_style': 'int',
        'background_color': 'int',
        'field_text': 'str',
        'font_family': 'str',
        'font_size': 'float',
        'opacity': 'float',
        'angle': 'float'
    }

    attribute_map = {
        'guid': 'Guid',
        'document_guid': 'DocumentGuid',
        'text': 'Text',
        'creator_guid': 'CreatorGuid',
        'creator_name': 'CreatorName',
        'creator_email': 'CreatorEmail',
        'box': 'Box',
        'page_number': 'PageNumber',
        'annotation_position': 'AnnotationPosition',
        'svg_path': 'SvgPath',
        'type': 'Type',
        'access': 'Access',
        'replies': 'Replies',
        'created_on': 'CreatedOn',
        'font_color': 'FontColor',
        'pen_color': 'PenColor',
        'pen_width': 'PenWidth',
        'pen_style': 'PenStyle',
        'background_color': 'BackgroundColor',
        'field_text': 'FieldText',
        'font_family': 'FontFamily',
        'font_size': 'FontSize',
        'opacity': 'Opacity',
        'angle': 'Angle'
    }

    def __init__(self, guid=None, document_guid=None, text=None, creator_guid=None, creator_name=None, creator_email=None, box=None, page_number=None, annotation_position=None, svg_path=None, type=None, access=None, replies=None, created_on=None, font_color=None, pen_color=None, pen_width=None, pen_style=None, background_color=None, field_text=None, font_family=None, font_size=None, opacity=None, angle=None, **kwargs):  # noqa: E501
        """Initializes new instance of AnnotationInfo"""  # noqa: E501

        self._guid = None
        self._document_guid = None
        self._text = None
        self._creator_guid = None
        self._creator_name = None
        self._creator_email = None
        self._box = None
        self._page_number = None
        self._annotation_position = None
        self._svg_path = None
        self._type = None
        self._access = None
        self._replies = None
        self._created_on = None
        self._font_color = None
        self._pen_color = None
        self._pen_width = None
        self._pen_style = None
        self._background_color = None
        self._field_text = None
        self._font_family = None
        self._font_size = None
        self._opacity = None
        self._angle = None

        if guid is not None:
            self.guid = guid
        if document_guid is not None:
            self.document_guid = document_guid
        if text is not None:
            self.text = text
        if creator_guid is not None:
            self.creator_guid = creator_guid
        if creator_name is not None:
            self.creator_name = creator_name
        if creator_email is not None:
            self.creator_email = creator_email
        if box is not None:
            self.box = box
        if page_number is not None:
            self.page_number = page_number
        if annotation_position is not None:
            self.annotation_position = annotation_position
        if svg_path is not None:
            self.svg_path = svg_path
        if type is not None:
            self.type = type
        if access is not None:
            self.access = access
        if replies is not None:
            self.replies = replies
        if created_on is not None:
            self.created_on = created_on
        if font_color is not None:
            self.font_color = font_color
        if pen_color is not None:
            self.pen_color = pen_color
        if pen_width is not None:
            self.pen_width = pen_width
        if pen_style is not None:
            self.pen_style = pen_style
        if background_color is not None:
            self.background_color = background_color
        if field_text is not None:
            self.field_text = field_text
        if font_family is not None:
            self.font_family = font_family
        if font_size is not None:
            self.font_size = font_size
        if opacity is not None:
            self.opacity = opacity
        if angle is not None:
            self.angle = angle
    
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
    def document_guid(self):
        """
        Gets the document_guid.  # noqa: E501

        Gets or sets the document unique identifier  # noqa: E501

        :return: The document_guid.  # noqa: E501
        :rtype: int
        """
        return self._document_guid

    @document_guid.setter
    def document_guid(self, document_guid):
        """
        Sets the document_guid.

        Gets or sets the document unique identifier  # noqa: E501

        :param document_guid: The document_guid.  # noqa: E501
        :type: int
        """
        if document_guid is None:
            raise ValueError("Invalid value for `document_guid`, must not be `None`")  # noqa: E501
        self._document_guid = document_guid
    
    @property
    def text(self):
        """
        Gets the text.  # noqa: E501

        Gets or sets the annotation text  # noqa: E501

        :return: The text.  # noqa: E501
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text.

        Gets or sets the annotation text  # noqa: E501

        :param text: The text.  # noqa: E501
        :type: str
        """
        self._text = text
    
    @property
    def creator_guid(self):
        """
        Gets the creator_guid.  # noqa: E501

        Gets or sets the creator unique identifier  # noqa: E501

        :return: The creator_guid.  # noqa: E501
        :rtype: str
        """
        return self._creator_guid

    @creator_guid.setter
    def creator_guid(self, creator_guid):
        """
        Sets the creator_guid.

        Gets or sets the creator unique identifier  # noqa: E501

        :param creator_guid: The creator_guid.  # noqa: E501
        :type: str
        """
        self._creator_guid = creator_guid
    
    @property
    def creator_name(self):
        """
        Gets the creator_name.  # noqa: E501

        Gets or sets the name of the creator  # noqa: E501

        :return: The creator_name.  # noqa: E501
        :rtype: str
        """
        return self._creator_name

    @creator_name.setter
    def creator_name(self, creator_name):
        """
        Sets the creator_name.

        Gets or sets the name of the creator  # noqa: E501

        :param creator_name: The creator_name.  # noqa: E501
        :type: str
        """
        self._creator_name = creator_name
    
    @property
    def creator_email(self):
        """
        Gets the creator_email.  # noqa: E501

        Gets or sets the creator's email  # noqa: E501

        :return: The creator_email.  # noqa: E501
        :rtype: str
        """
        return self._creator_email

    @creator_email.setter
    def creator_email(self, creator_email):
        """
        Sets the creator_email.

        Gets or sets the creator's email  # noqa: E501

        :param creator_email: The creator_email.  # noqa: E501
        :type: str
        """
        self._creator_email = creator_email
    
    @property
    def box(self):
        """
        Gets the box.  # noqa: E501

        Gets or sets the box where annotation will be placed  # noqa: E501

        :return: The box.  # noqa: E501
        :rtype: Rectangle
        """
        return self._box

    @box.setter
    def box(self, box):
        """
        Sets the box.

        Gets or sets the box where annotation will be placed  # noqa: E501

        :param box: The box.  # noqa: E501
        :type: Rectangle
        """
        if box is None:
            raise ValueError("Invalid value for `box`, must not be `None`")  # noqa: E501
        self._box = box
    
    @property
    def page_number(self):
        """
        Gets the page_number.  # noqa: E501

        Gets or sets the number of page where annotation will be placed  # noqa: E501

        :return: The page_number.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """
        Sets the page_number.

        Gets or sets the number of page where annotation will be placed  # noqa: E501

        :param page_number: The page_number.  # noqa: E501
        :type: int
        """
        self._page_number = page_number
    
    @property
    def annotation_position(self):
        """
        Gets the annotation_position.  # noqa: E501

        Gets or sets the annotation position  # noqa: E501

        :return: The annotation_position.  # noqa: E501
        :rtype: Point
        """
        return self._annotation_position

    @annotation_position.setter
    def annotation_position(self, annotation_position):
        """
        Sets the annotation_position.

        Gets or sets the annotation position  # noqa: E501

        :param annotation_position: The annotation_position.  # noqa: E501
        :type: Point
        """
        self._annotation_position = annotation_position
    
    @property
    def svg_path(self):
        """
        Gets the svg_path.  # noqa: E501

        Gets or sets the annotation SVG path  # noqa: E501

        :return: The svg_path.  # noqa: E501
        :rtype: str
        """
        return self._svg_path

    @svg_path.setter
    def svg_path(self, svg_path):
        """
        Sets the svg_path.

        Gets or sets the annotation SVG path  # noqa: E501

        :param svg_path: The svg_path.  # noqa: E501
        :type: str
        """
        self._svg_path = svg_path
    
    @property
    def type(self):
        """
        Gets the type.  # noqa: E501

        Gets or sets the annotation type  # noqa: E501

        :return: The type.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type.

        Gets or sets the annotation type  # noqa: E501

        :param type: The type.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["Text", "Area", "Point", "TextStrikeout", "Polyline", "TextField", "Watermark", "TextReplacement", "Arrow", "TextRedaction", "ResourcesRedaction", "TextUnderline", "Distance", "Ellipse"]  # noqa: E501
        if not type.isdigit():	
            if type not in allowed_values:
                raise ValueError(
                    "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                    .format(type, allowed_values))
            self._type = type
        else:
            self._type = allowed_values[int(type) if six.PY3 else long(type)]
    
    @property
    def access(self):
        """
        Gets the access.  # noqa: E501

        Gets or sets the annotation access  # noqa: E501

        :return: The access.  # noqa: E501
        :rtype: str
        """
        return self._access

    @access.setter
    def access(self, access):
        """
        Sets the access.

        Gets or sets the annotation access  # noqa: E501

        :param access: The access.  # noqa: E501
        :type: str
        """
        allowed_values = ["Public", "Private"]  # noqa: E501
        if not access.isdigit():	
            if access not in allowed_values:
                raise ValueError(
                    "Invalid value for `access` ({0}), must be one of {1}"  # noqa: E501
                    .format(access, allowed_values))
            self._access = access
        else:
            self._access = allowed_values[int(access) if six.PY3 else long(access)]
    
    @property
    def replies(self):
        """
        Gets the replies.  # noqa: E501

        Gets or sets the array of annotation replies  # noqa: E501

        :return: The replies.  # noqa: E501
        :rtype: list[AnnotationReplyInfo]
        """
        return self._replies

    @replies.setter
    def replies(self, replies):
        """
        Sets the replies.

        Gets or sets the array of annotation replies  # noqa: E501

        :param replies: The replies.  # noqa: E501
        :type: list[AnnotationReplyInfo]
        """
        self._replies = replies
    
    @property
    def created_on(self):
        """
        Gets the created_on.  # noqa: E501

        Gets or sets the annotation created on date  # noqa: E501

        :return: The created_on.  # noqa: E501
        :rtype: datetime
        """
        return self._created_on

    @created_on.setter
    def created_on(self, created_on):
        """
        Sets the created_on.

        Gets or sets the annotation created on date  # noqa: E501

        :param created_on: The created_on.  # noqa: E501
        :type: datetime
        """
        if created_on is None:
            raise ValueError("Invalid value for `created_on`, must not be `None`")  # noqa: E501
        self._created_on = created_on
    
    @property
    def font_color(self):
        """
        Gets the font_color.  # noqa: E501

        Gets or sets the annotation's font color  # noqa: E501

        :return: The font_color.  # noqa: E501
        :rtype: int
        """
        return self._font_color

    @font_color.setter
    def font_color(self, font_color):
        """
        Sets the font_color.

        Gets or sets the annotation's font color  # noqa: E501

        :param font_color: The font_color.  # noqa: E501
        :type: int
        """
        self._font_color = font_color
    
    @property
    def pen_color(self):
        """
        Gets the pen_color.  # noqa: E501

        Gets or sets the annotation's pen color  # noqa: E501

        :return: The pen_color.  # noqa: E501
        :rtype: int
        """
        return self._pen_color

    @pen_color.setter
    def pen_color(self, pen_color):
        """
        Sets the pen_color.

        Gets or sets the annotation's pen color  # noqa: E501

        :param pen_color: The pen_color.  # noqa: E501
        :type: int
        """
        self._pen_color = pen_color
    
    @property
    def pen_width(self):
        """
        Gets the pen_width.  # noqa: E501

        Gets or sets the annotation's pen width  # noqa: E501

        :return: The pen_width.  # noqa: E501
        :rtype: int
        """
        return self._pen_width

    @pen_width.setter
    def pen_width(self, pen_width):
        """
        Sets the pen_width.

        Gets or sets the annotation's pen width  # noqa: E501

        :param pen_width: The pen_width.  # noqa: E501
        :type: int
        """
        self._pen_width = pen_width
    
    @property
    def pen_style(self):
        """
        Gets the pen_style.  # noqa: E501

        Gets or sets the annotation's pen style  # noqa: E501

        :return: The pen_style.  # noqa: E501
        :rtype: int
        """
        return self._pen_style

    @pen_style.setter
    def pen_style(self, pen_style):
        """
        Sets the pen_style.

        Gets or sets the annotation's pen style  # noqa: E501

        :param pen_style: The pen_style.  # noqa: E501
        :type: int
        """
        self._pen_style = pen_style
    
    @property
    def background_color(self):
        """
        Gets the background_color.  # noqa: E501

        Gets or sets the annotation's background color   # noqa: E501

        :return: The background_color.  # noqa: E501
        :rtype: int
        """
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        """
        Sets the background_color.

        Gets or sets the annotation's background color   # noqa: E501

        :param background_color: The background_color.  # noqa: E501
        :type: int
        """
        self._background_color = background_color
    
    @property
    def field_text(self):
        """
        Gets the field_text.  # noqa: E501

        Gets or sets the annotation's field text  # noqa: E501

        :return: The field_text.  # noqa: E501
        :rtype: str
        """
        return self._field_text

    @field_text.setter
    def field_text(self, field_text):
        """
        Sets the field_text.

        Gets or sets the annotation's field text  # noqa: E501

        :param field_text: The field_text.  # noqa: E501
        :type: str
        """
        self._field_text = field_text
    
    @property
    def font_family(self):
        """
        Gets the font_family.  # noqa: E501

        Gets or sets the annotation's font family  # noqa: E501

        :return: The font_family.  # noqa: E501
        :rtype: str
        """
        return self._font_family

    @font_family.setter
    def font_family(self, font_family):
        """
        Sets the font_family.

        Gets or sets the annotation's font family  # noqa: E501

        :param font_family: The font_family.  # noqa: E501
        :type: str
        """
        self._font_family = font_family
    
    @property
    def font_size(self):
        """
        Gets the font_size.  # noqa: E501

        Gets or sets the annotation's font size   # noqa: E501

        :return: The font_size.  # noqa: E501
        :rtype: float
        """
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        """
        Sets the font_size.

        Gets or sets the annotation's font size   # noqa: E501

        :param font_size: The font_size.  # noqa: E501
        :type: float
        """
        self._font_size = font_size
    
    @property
    def opacity(self):
        """
        Gets the opacity.  # noqa: E501

        Gets or sets the annotation's opacity  # noqa: E501

        :return: The opacity.  # noqa: E501
        :rtype: float
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        """
        Sets the opacity.

        Gets or sets the annotation's opacity  # noqa: E501

        :param opacity: The opacity.  # noqa: E501
        :type: float
        """
        self._opacity = opacity
    
    @property
    def angle(self):
        """
        Gets the angle.  # noqa: E501

        Gets or sets the watermark annotation's rotation angle  # noqa: E501

        :return: The angle.  # noqa: E501
        :rtype: float
        """
        return self._angle

    @angle.setter
    def angle(self, angle):
        """
        Sets the angle.

        Gets or sets the watermark annotation's rotation angle  # noqa: E501

        :param angle: The angle.  # noqa: E501
        :type: float
        """
        self._angle = angle

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
        if not isinstance(other, AnnotationInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
