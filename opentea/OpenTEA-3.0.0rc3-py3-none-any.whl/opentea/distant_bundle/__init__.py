#!/usr/bin/env python

# Check python version
import sys
if ((sys.hexversion < 0x020606F0) or
    (sys.hexversion > 0x030000A0)):
    raise Exception(
            "Must be run with python version at least 2.6.6, and not python 3\n"
            "Your version is %i.%i.%i" % sys.version_info[:3])

# Constants and exceptions First
from .constants import *
from .exceptions import (XDRException, XDRnoNodeException,
                         XDRtooManyNodesException, XDRnoFileException, 
                         XDRillFormed)

### XXX This is ugly, but can't find a workaround...
# Should be simply :
# from .log import *
# However, in that case, the log output to the console is ok, but not in a file.
# Can't find out why...
# Simple logging
import logging
logger = logging.getLogger()
logger.setLevel("DEBUG")
LOG_LEVEL_FILE = "DEBUG"
LOG_LEVEL_STREAM = "DEBUG"

file_format = logging.Formatter("%(asctime)s %(name)s %(levelname)s  %(message)s")
file_handler = logging.FileHandler(__name__+'.log')
file_handler.setFormatter(file_format)
file_handler.setLevel(LOG_LEVEL_FILE)
logger.addHandler(file_handler)

stream_format = logging.Formatter("%(levelname)s  %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(stream_format)
stream_handler.setLevel(LOG_LEVEL_STREAM)
logger.addHandler(stream_handler)

# PathTools and Dataset only inherit from object
from .path_tools import PathTools
from .dataset import Dataset

# Additional distant tools
from .distanttools import DistantTools
