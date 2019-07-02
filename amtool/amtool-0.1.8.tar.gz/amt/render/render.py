"""
amt-render -- Artifact Management Tool Reader

amt is a Tool for managing software artifacts

It defines classes_and_methods and a command line interface

@author:     Kenneth E. Bellock

@copyright:

@contact:    ken@bellock.net

"""
import os
import sys
import copy
import logging
from mako.template import Template
from mako import exceptions


__all__ = ['render', 'rendernode']
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(SCRIPT_PATH), 'load'))
sys.path.insert(0, os.path.join(os.path.dirname(SCRIPT_PATH), 'uid'))
from load import load
from uid import uid


def rendernode(value, uids):
    """
    The node renderer.  This is a mako template implementation of a node
    renderer, but is intended to be overwritten by users wanting to use a
    different rendering engine.

    `Note:  If there is any error during the rendering of a node, it should be
    logged as an error, and the original content of the node must be returned.`

    Args:
        value (string): The content of the node to be rendered in the artifacts
                     tree.

        uids (dict): Map of artifacts to unique identifiers.

    Returns:

        string: The renderend node.
    """
    try:
        return Template(value).render(UID=uids)
    except:
        logging.error(exceptions.text_error_template().render())
        return value


def _render(artifacts, uids):
    """
    Recursive helper function for diving into dictionaries of dictionaries
    searching for unique id's.

    Args:
        artifacts (dict): Input dictionary.

        uids (dict): Map of artifacts to unique identifiers.

    Returns:
        dict: returned dictionary
    """
    if isinstance(artifacts, dict):
        for key, value in artifacts.items():
            if isinstance(value, (dict, list, tuple)):
                _render(value, uids)
            elif isinstance(value, str):
                artifacts[key] = rendernode(value, uids)
    elif isinstance(artifacts, (list, tuple)):
        for index, value in enumerate(artifacts):
            if isinstance(value, (dict, list, tuple)):
                _render(value, uids)
            elif isinstance(value, str):
                artifacts[index] = Template(value).render(UID=uids)


def render(source):
    """
    Render a set of artifacts.

    The `target` can be a directory or file, and can contain plain yaml, or
    canonicalized artifact data.  If a directory is specified, it will be
    walked recursively and all files will be loaded into the return data
    structure.

    Args:
        source (string): The directory or file to be loaded.

    Returns:
        dict.  The fully read data structure containing all artifacts from the
        loaded target.
    """
    logging.debug('Rendering: %s', source)
    if isinstance(source, str):
        data = load(source)
    else:
        data = copy.deepcopy(source)
    _render({'': data}, uid(source))
    return data
