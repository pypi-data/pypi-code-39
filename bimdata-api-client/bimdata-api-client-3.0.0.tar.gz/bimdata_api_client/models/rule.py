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


class Rule(object):
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
        'name': 'str',
        'condition': 'str',
        'rule_components': 'list[RuleComponent]',
        'on': 'Rule'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'condition': 'condition',
        'rule_components': 'rule_components',
        'on': 'on'
    }

    def __init__(self, id=None, name=None, condition=None, rule_components=None, on=None):  # noqa: E501
        """Rule - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._name = None
        self._condition = None
        self._rule_components = None
        self._on = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        self.condition = condition
        if rule_components is not None:
            self.rule_components = rule_components
        if on is not None:
            self.on = on

    @property
    def id(self):
        """Gets the id of this Rule.  # noqa: E501


        :return: The id of this Rule.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Rule.


        :param id: The id of this Rule.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Rule.  # noqa: E501


        :return: The name of this Rule.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Rule.


        :param name: The name of this Rule.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def condition(self):
        """Gets the condition of this Rule.  # noqa: E501


        :return: The condition of this Rule.  # noqa: E501
        :rtype: str
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """Sets the condition of this Rule.


        :param condition: The condition of this Rule.  # noqa: E501
        :type: str
        """
        if condition is None:
            raise ValueError("Invalid value for `condition`, must not be `None`")  # noqa: E501
        if condition is not None and len(condition) < 1:
            raise ValueError("Invalid value for `condition`, length must be greater than or equal to `1`")  # noqa: E501

        self._condition = condition

    @property
    def rule_components(self):
        """Gets the rule_components of this Rule.  # noqa: E501


        :return: The rule_components of this Rule.  # noqa: E501
        :rtype: list[RuleComponent]
        """
        return self._rule_components

    @rule_components.setter
    def rule_components(self, rule_components):
        """Sets the rule_components of this Rule.


        :param rule_components: The rule_components of this Rule.  # noqa: E501
        :type: list[RuleComponent]
        """

        self._rule_components = rule_components

    @property
    def on(self):
        """Gets the on of this Rule.  # noqa: E501


        :return: The on of this Rule.  # noqa: E501
        :rtype: Rule
        """
        return self._on

    @on.setter
    def on(self, on):
        """Sets the on of this Rule.


        :param on: The on of this Rule.  # noqa: E501
        :type: Rule
        """

        self._on = on

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
        if not isinstance(other, Rule):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
