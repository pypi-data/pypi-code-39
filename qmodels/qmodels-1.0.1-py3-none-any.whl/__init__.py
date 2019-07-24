"""Simulation of queuing models with simulus."""

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 8):
    raise ImportError("QModels requires Python 2.8 and above (%d.%d detected)." %
                      sys.version_info[:2])
del sys

from .rng import *
from .mm1 import *

__version__ = '1.0.1'
