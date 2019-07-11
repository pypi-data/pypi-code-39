"""pylint_boxwisemaatwerl module."""
from __future__ import absolute_import

import sys

from pylint_boxwisemaatwerk import plugin

register = plugin.register  # pylint: disable=invalid-name

# we are not using load.configuration since we are not transforming basecheckers
# load_configuration = plugin.load_configuration  # pylint: disable=invalid-name
