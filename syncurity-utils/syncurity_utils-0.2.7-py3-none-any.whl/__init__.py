""" Syncurity Utils package

This package provides a common library of utilities and models that are useful across Syncurity's library of Stackstorm
packs.

:copyright: (c) 2019 Syncurity
:license: Apache 2.0, see LICENSE.txt for more details
"""

from .__version__ import __title__, __description__, __version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__

# Default logger configuration
import logging
from logging import NullHandler

# TODO: import all explicitly
from .typecheck import typecheck
from .models import *
from .api import send_facts
# Classes
from .utils import DecodeProofpointURL

# Functions
from .utils import find_domain

logging.getLogger(__name__).addHandler(NullHandler())
