"""
independent chemical symbols
"""


__version__ = '1.6.0'
def version():
    return __version__

from . import name, unit, geo
from . import file, string, system
from . import types

from .status import Status



