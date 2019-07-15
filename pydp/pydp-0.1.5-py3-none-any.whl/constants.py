#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: constants.py
Desc: 系统常量
      *注：此文件为基础lib，不可依赖其他任何dp库，以避免出现引用环
Author:yanjingang(yanjingang@mail.com)
Date: 2019/2/21 23:34
"""
import os

# 项目根目录
APP_PATH = os.path.dirname(os.path.abspath(__file__))
#APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

# 数据文件目录
DATA_PATH = APP_PATH + '/data'

# 当前用户系统根目录
USER_PATH = os.path.expanduser('~')

# 临时目录
TEMP_PATH = '/tmp'


if __name__ == '__main__':
    """test"""
    print("APP_PATH: {}".format(APP_PATH))
    print("DATA_PATH: {}".format(DATA_PATH))
    print("USER_PATH: {}".format(USER_PATH))
    print("TEMP_PATH: {}".format(TEMP_PATH))
