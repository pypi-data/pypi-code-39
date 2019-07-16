# -*- coding: utf-8 -*-
from os import sep
from functools import partial

import six
import yaml

from sceptre.exceptions import PathConversionError


def get_external_stack_name(project_code, stack_name):
    """
    Returns the name given to a stack in CloudFormation.
    :param project_code: The project code, as defined in config.yaml.
    :type project_code: str
    :param stack_name: The name of the stack.
    :type stack_name: str
    :returns: The name given to the stack in CloudFormation.
    :rtype: str
    """
    return "-".join([
        project_code,
        stack_name.replace("/", "-")
    ])


def mask_key(key):
    """
    Returns an masked version of ``key``.

    Returned version has all but the last four characters are replaced with the
    character "*".

    :param key: The string to mask.
    :type key: str
    :returns: An masked version of the key
    :rtype: str
    """
    num_mask_chars = len(key) - 4

    return "".join([
        "*" if i < num_mask_chars else c
        for i, c in enumerate(key)
    ])


def _call_func_on_values(func, attr, cls):
    """
    Searches through dictionary or list for objects of type `cls` and calls the
    supplied function `func`. Supports nested dictionaries and lists.
    Does not detect objects used as keys in dictionaries.

    :param attr: A dictionary or list to search through.
    :type attr: dict or list
    :return: The dictionary or list structure.
    :rtype: dict or list
    """

    def func_on_instance(key):
        if isinstance(value, cls):
            func(attr, key, value)
        elif isinstance(value, list) or isinstance(value, dict):
            _call_func_on_values(func, value, cls)

    if isinstance(attr, dict):
        for key, value in attr.items():
            func_on_instance(key)
    elif isinstance(attr, list):
        for index, value in enumerate(attr):
            func_on_instance(index)
    return attr


def normalise_path(path):
    """
    Converts a path to use correct path separator.
    Raises an PathConversionError if the path has a
    trailing slash.
    :param path: A directory path
    :type path: str
    :raises: sceptre.exceptions.PathConversionError
    :returns: A normalised path with forward slashes.
    :returns: string
    """
    if sep is '/':
        path = path.replace('\\', '/')
    elif sep is '\\':
        path = path.replace('/', '\\')
    if path.endswith("/") or path.endswith("\\"):
        raise PathConversionError(
            "'{0}' is an invalid path string. Paths should "
            "not have trailing slashes.".format(path)
        )
    return path


def sceptreise_path(path):
    """
    Converts a path to use correct sceptre path separator.
    Raises an PathConversionError if the path has a
    trailing slash.
    :param path: A directory path
    :type path: str
    :raises: sceptre.exceptions.PathConversionError
    :returns: A normalised path with forward slashes.
    :returns: string
    """
    path = path.replace('\\', '/')
    if path.endswith("/") or path.endswith("\\"):
        raise PathConversionError(
            "'{0}' is an invalid path string. Paths should "
            "not have trailing slashes.".format(path)
        )
    return path


CFN_FNS = [
    'And',
    'Base64',
    'Cidr',
    'Equals',
    'FindInMap',
    'GetAtt',
    'GetAZs',
    'If',
    'ImportValue',
    'Join',
    'Not',
    'Or',
    'Select',
    'Split',
    'Sub',
    'Transform',
]

CFN_TAGS = [
    'Condition',
    'Ref',
]


def _getatt_constructor(loader, node):
    if isinstance(node.value, six.text_type):
        return node.value.split('.', 1)
    elif isinstance(node.value, list):
        seq = loader.construct_sequence(node)
        for item in seq:
            if not isinstance(item, six.text_type):
                raise ValueError(
                    "Fn::GetAtt does not support complex datastructures")
        return seq
    else:
        raise ValueError("Fn::GetAtt only supports string or list values")


def _tag_constructor(loader, tag_suffix, node):
    if tag_suffix not in CFN_FNS and tag_suffix not in CFN_TAGS:
        raise ValueError("Bad tag: !{tag_suffix}. Supported tags are: "
                         "{supported_tags}".format(
                             tag_suffix=tag_suffix,
                             supported_tags=", ".join(sorted(CFN_TAGS + CFN_FNS))
                         ))

    if tag_suffix in CFN_FNS:
        tag_suffix = "Fn::{tag_suffix}".format(tag_suffix=tag_suffix)

    data = {}
    yield data

    if tag_suffix == 'Fn::GetAtt':
        constructor = partial(_getatt_constructor, (loader, ))
    elif isinstance(node, yaml.ScalarNode):
        constructor = loader.construct_scalar
    elif isinstance(node, yaml.SequenceNode):
        constructor = loader.construct_sequence
    elif isinstance(node, yaml.MappingNode):
        constructor = loader.construct_mapping

    data[tag_suffix] = constructor(node)


class CfnYamlLoader(yaml.SafeLoader):
    pass


CfnYamlLoader.add_multi_constructor("!", _tag_constructor)
