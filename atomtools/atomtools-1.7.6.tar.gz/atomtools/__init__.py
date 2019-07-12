"""
independent chemical symbols
"""


__version__ = '1.7.6'
def version():
    return __version__

from . import name, unit, geo
from . import file, string, system
from . import types
from .filetype import filetype, list_supported_formats, support_multiframe
from .status import Status
