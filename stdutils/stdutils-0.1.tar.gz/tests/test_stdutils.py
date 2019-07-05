#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# date:        2019/7/5
# author:      he.zhiming
#

from __future__ import (absolute_import, unicode_literals)

from stdutils import *
import pytest

@pytest.mark.usefixtures("filename")
def test_rm(filename):
    rm(filename)


def test_mv(filename):
    mv(filename, './')