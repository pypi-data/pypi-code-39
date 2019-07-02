#!/usr/bin/python
# encoding: utf-8
"""
amt-io -- Artifact Management Tool Input/Output

amt is a Tool for managing software artifacts

It defines classes_and_methods and a command line interface

@author:     Kenneth E. Bellock

@copyright:

@contact:    ken@bellock.net

"""
import yaml
from collections import OrderedDict

__all__ = ['load', 'dump', 'safe_load', 'safe_dump']


def load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            list(data.items()))
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


def safe_load(stream, object_pairs_hook=OrderedDict):
    return load(stream, yaml.SafeLoader, object_pairs_hook)


def safe_dump(data, stream=None, **kwds):
    return dump(data, Dumper=yaml.SafeDumper, **kwds)
