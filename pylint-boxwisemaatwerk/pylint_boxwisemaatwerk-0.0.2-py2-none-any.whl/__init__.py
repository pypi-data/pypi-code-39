"""pylint_boxwisemaatwerl module."""
from __future__ import absolute_import

import sys

import boxwise_pluginplugin

register = boxwise_plugin.register  # pylint: disable=invalid-name

# we are not using load.configuration since we are not transforming basecheckers
# load_configuration = plugin.load_configuration  # pylint: disable=invalid-name
