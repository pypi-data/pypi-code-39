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


class PropertyDefinition(object):
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
        'unit': 'Unit',
        'name': 'str',
        'description': 'str',
        'type': 'str',
        'value_type': 'str'
    }

    attribute_map = {
        'id': 'id',
        'unit': 'unit',
        'name': 'name',
        'description': 'description',
        'type': 'type',
        'value_type': 'value_type'
    }

    def __init__(self, id=None, unit=None, name=None, description=None, type=None, value_type=None):  # noqa: E501
        """PropertyDefinition - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._unit = None
        self._name = None
        self._description = None
        self._type = None
        self._value_type = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if unit is not None:
            self.unit = unit
        self.name = name
        self.description = description
        self.type = type
        self.value_type = value_type

    @property
    def id(self):
        """Gets the id of this PropertyDefinition.  # noqa: E501


        :return: The id of this PropertyDefinition.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PropertyDefinition.


        :param id: The id of this PropertyDefinition.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def unit(self):
        """Gets the unit of this PropertyDefinition.  # noqa: E501


        :return: The unit of this PropertyDefinition.  # noqa: E501
        :rtype: Unit
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Sets the unit of this PropertyDefinition.


        :param unit: The unit of this PropertyDefinition.  # noqa: E501
        :type: Unit
        """

        self._unit = unit

    @property
    def name(self):
        """Gets the name of this PropertyDefinition.  # noqa: E501


        :return: The name of this PropertyDefinition.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PropertyDefinition.


        :param name: The name of this PropertyDefinition.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this PropertyDefinition.  # noqa: E501


        :return: The description of this PropertyDefinition.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PropertyDefinition.


        :param description: The description of this PropertyDefinition.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def type(self):
        """Gets the type of this PropertyDefinition.  # noqa: E501

        IfcProperty*, Ifc*Properties, IfcComplexProperty, IfcQuantity*, IfcComplexQuantity, Attribute  # noqa: E501

        :return: The type of this PropertyDefinition.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this PropertyDefinition.

        IfcProperty*, Ifc*Properties, IfcComplexProperty, IfcQuantity*, IfcComplexQuantity, Attribute  # noqa: E501

        :param type: The type of this PropertyDefinition.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def value_type(self):
        """Gets the value_type of this PropertyDefinition.  # noqa: E501

        Type of the corresponding value (Boolean, integer, float, string, IfcRange, ...)  # noqa: E501

        :return: The value_type of this PropertyDefinition.  # noqa: E501
        :rtype: str
        """
        return self._value_type

    @value_type.setter
    def value_type(self, value_type):
        """Sets the value_type of this PropertyDefinition.

        Type of the corresponding value (Boolean, integer, float, string, IfcRange, ...)  # noqa: E501

        :param value_type: The value_type of this PropertyDefinition.  # noqa: E501
        :type: str
        """

        self._value_type = value_type

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
        if not isinstance(other, PropertyDefinition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
