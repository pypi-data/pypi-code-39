"""
amt-canonical -- Artifact Management Tool Reader

amt is a Tool for managing software artifacts

It defines classes_and_methods and a command line interface

@author:     Kenneth E. Bellock

@copyright:

@contact:    ken@bellock.net

"""
import os
import sys

__all__ = ['canonical']
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = os.path.join(SCRIPT_PATH, '..', '..')
sys.path.insert(0, LIB_PATH)
from amt.load import load
from amt.save import save


def canonical(path):
    """
    Enforce a canonical representation of the artifact tree.

    When directly working with artifact trees, there are many different
    representations of formatting that will result in the same artifact tree.
    This can cause issues when colaboratively working an atrifact tree within a
    version control system.  This function will return a consistently formatted
    artifact tree to ensure no user specific style is captured.

    Args:
        path (str):  The artifact tree location.

    Returns:
        string: A canonical representation of the input artifacts tree.
    """
    save(path, load(path))
