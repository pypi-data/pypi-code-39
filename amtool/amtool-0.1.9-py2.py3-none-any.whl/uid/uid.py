"""
amt-uid -- Artifact Management Tool Reader

amt is a Tool for managing software artifacts

It defines classes_and_methods and a command line interface

@author:     Kenneth E. Bellock

@copyright:

@contact:    ken@bellock.net

"""
import os
import sys
import uuid
import logging

__all__ = ['uid', 'newuid']
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(SCRIPT_PATH), 'load'))
from load import load


def newuid():
    """
    Get a unique id string.

    Returns:
       string: A unique id string.
    """
    return uuid.uuid4().hex


def _uid(artifacts):
    """
    Recursive helper function for diving into dictionaries of dictionaries
    searching for unique id's.

    Args:
        artifacts (dict): Input dictionary.

    Returns:
        dict: Returned dictionary.
    """
    results = {}
    if isinstance(artifacts, dict):
        for key, value in artifacts.items():
            if isinstance(value, dict):
                results = {**results, **_uid(value)}
        lower = {key.lower(): value for key, value in artifacts.items()}
        if 'uid' in lower:
            results[lower['uid']] = artifacts
    return results


def uid(source):
    """
    Return a dictionary of unique id's.

    The entire data structure loaded from the given source will be searched for
    unique id's, and a dictionary will be returned that contains all the unique
    id's as keys, and the source document as a value.

    Args:
        source (str or dict): A path to a file or directory or a dictionary
        containing documenents with unique id's.

    Returns:
        dict:  The return dictioanry.
    """
    logging.debug('Creating uid map: %s', source)
    if isinstance(source, str):
        data = load(source)
    else:
        data = source
    return _uid(data)
