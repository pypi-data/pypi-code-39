#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# date:        2019/7/4
# author:      he.zhiming
#

from __future__ import (absolute_import, unicode_literals)

import shutil
from os.path import (isfile, isdir, abspath, exists)
import os


class StdUtilError(Exception):
    pass


def rm(p):
    """rm一个文件或者目录

    :param p: 文件或者目录
    :return:
    """
    if isfile(p):
        os.remove(p)
    elif isdir(p):
        shutil.rmtree(p)
    else:
        raise StdUtilError(f'{p} must be a file or dir')


def cp(src, dst):
    """拷贝文件或者目录

    :param src: 文件/目录
    :param dst: 文件/目录
    :return:
    """
    if isfile(src):
        shutil.copy(src, dst)
    else:
        if not exists(dst):
            shutil.copytree(src, dst)
        else:
            raise StdUtilError('dst must not already exists!')


def mv(src, dst):
    """mv文件或者目录

    :param src: 文件/目录
    :param dst: 文件/目录
    :return:
    """
    shutil.move(src, dst)
