"""
independent chemical symbols
"""


__version__ = '1.7.2'
def version():
    return __version__

from . import name, unit, geo
from . import file, string, system
from . import types
from .filetype import filetype, list_supported_formats
from .status import Status



