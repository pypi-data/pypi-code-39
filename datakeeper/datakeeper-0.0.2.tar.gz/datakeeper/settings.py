import yaml
from os import path
from attrdict import AttrDict

from datakeeper.utility import relpath
from datakeeper.io import read

specs = {}
"""dict: keys are component names; values are a `dict` with component specs.
"""

def load(specfile):
    """Recursively loads the specificied specfile into a :class:`attrdict.AttrDict`.

    Args:
        specfile (str): path to the specification YML file; may be relative.
    """
    context, sfile = path.split(path.abspath(specfile))
    spec = read(context, path.splitext(sfile)[0])
    return AttrDict(spec)
