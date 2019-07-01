"""ajgar.py: Main module.

"""
from __future__ import print_function, division, absolute_import
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__license__          = "GNU GPL"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

try:
    # This depends on scipy
    from dilawar.data_analysis import *
except ImportError:
    pass

from dilawar.text_processing import *
from dilawar.file_utils import *
from dilawar.plot_utils import *
from dilawar.statistics import *
from dilawar.information_theory import *
from dilawar.io_utils import *
from dilawar.logger import *
from dilawar.brian_utils import *
