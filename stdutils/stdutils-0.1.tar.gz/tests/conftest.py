#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# date:        2019/7/5
# author:      he.zhiming
#

from __future__ import (absolute_import, unicode_literals)

import pytest
import os


@pytest.fixture(params=['file1', 'file2', 'file3'])
def filename(request, tmpdir):
    """制造一个临时文件

    :param request:
    :param tmpdir:
    :return:
    """
    filename = request.param
    filepath = str(tmpdir.join(filename))

    with open(filepath, mode='w', encoding='utf-8') as f:
        f.write(filepath)

    yield filepath


