__all__ = ['data', 'run', 'analysis', 'lib', 'utils', 'path', 'plots'
           'simulation', 'esxresource']

from . import data
from . import run
from . import path
from . import utils
from . import lib
from . import simulation
from . import analysis
from . import plots
from . import esxresource

import os
import sys


def _get_resource(filename):
    """Upload as a file a resource located in the pyesx/lib/ directory
    """
    d = os.path.dirname(sys.modules['pyesx'].__file__)
    return open(os.join.join(d, '/lib/RUN_ex.sh'), 'rb')
