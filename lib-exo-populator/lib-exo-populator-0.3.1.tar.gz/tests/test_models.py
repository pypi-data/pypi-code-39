#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lib-exo-populator
------------

Tests for `lib-exo-populator` models module.
"""

from django.test import TestCase

from populate import models     # noqa
from stringcase import *    # noqa
from singleton_decorator import singleton   # noqa


class TestPopulate(TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass
