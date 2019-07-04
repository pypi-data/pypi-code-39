# -*- coding: utf-8 -*-

# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2018 Pol Canelles <canellestudi@gmail.com>

"""
Test cases for `~coherence.web.ui`

.. warning:: All the tests done here are without testing a real web socket
             connection. All the calls made to ws are fake calls, cause we
             depend on a real web browser with web sockets enabled. So, all
             java script responses are not tested here.
"""

from os.path import dirname
from coherence import log
from coherence import backends
# from coherence.extern.simple_plugin import Reception
logger = log.get_logger('simple_plugin')
logger.setLevel('INFO')
# rec = Reception(plugin_path=dirname(backends.__file__), log=logger)
# print(rec.guestlist())

from coherence import __version__
import coherence.base as base
base.pkg_resources = None

from twisted.internet.defer import inlineCallbacks
from twisted.trial import unittest


class SimplePluginTest(unittest.TestCase):
    # def setUp(self):
    #     self.plugins_reception = Reception(
    #         plugin_path=dirname(backends.__file__))
    #     self.coherence = base.Coherence(
    #         {'unittest': 'yes',
    #          'logmode': 'info',
    #          }
    #     )

    def test_plugins(self):
        plugins = base.Plugins()
        self.assertIsInstance(plugins, base.Plugins)
