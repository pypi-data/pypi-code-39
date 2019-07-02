"""
amt-load -- Artifact Management Tool Reader

amt is a Tool for managing software artifacts

It defines classes_and_methods and a command line interface

@author:     Kenneth E. Bellock

@copyright:

@contact:    ken@bellock.net

"""
import os
import sys
import yaml
import logging

__all__ = ['load']
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(SCRIPT_PATH), 'meta'))
from meta import MetaDict
from meta import MetaList


def _load_file(filename):
    """
    Loads a file into the specified node of the artifacts tree.

    This function is a helper function to `load`.  It processes a single
    artifact file for inclusion into the overall artifacts tree.

    Args:
        result: (dict): Node to load artifacts into.

        filename: (str): File to load artifacts from.

    Kwargs:
        verbose (int): Level to perform logging at.
    """
    logging.debug('Loading File: %s', filename)
    with open(filename, 'r') as f_obj:
        loaded_file_content = yaml.full_load(f_obj)
    logging.debug('Loaded File Content: %s', loaded_file_content)
    if isinstance(loaded_file_content, dict):
        metadict = MetaDict()
        metadict.update(loaded_file_content)
        metadict._file = filename
        return metadict
    if isinstance(loaded_file_content, (list, set, tuple)):
        metadict = MetaList()
        metadict.extend(loaded_file_content)
        metadict._file = filename
        return metadict


def load(target, toplevel=True):
    """
    Load a directory or file containing artifacts.

    The `target` can be a directory or file, and can contain plain yaml, or
    canonicalized artifact data.  If a directory is specified, it will be
    walked recursively and all files will be loaded into the return data
    structure.

    Args:
        target (str): The directory or file to be loaded.
        toplevel (bool, optional): Utilized in recursive operations with this
            function.

    Returns:
        dict or list or string:  The fully read data structure containing all
            artifacts from the loaded target.
    """
    logging.debug('Loading Target: %s', target)
    basename = os.path.basename(target)
    if os.path.isfile(target):
        if toplevel:
            return _load_file(target)
        else:
            return {os.path.splitext(basename)[0]: _load_file(target)}
    elif os.path.isdir(target):
        result = {}
        for path in os.listdir(target):
            result.update(load(os.path.join(target, path), toplevel=False))
        if toplevel:
            return result
        else:
            return {basename: result}
