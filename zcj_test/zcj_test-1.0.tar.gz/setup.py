# -*- coding: utf-8 -*-
# python_test
# @Time    : 2019/7/14 0014 14:12
# @Author  : 曾经

from distutils.core import setup

setup(
    name='zcj_test',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='这是第一个对外发布的模块，用于测试哦',  # 描述
    author='zcj',  # 作者
    author_email='969351379@qq.com',
    py_modules=['zcj_test.demo2', 'zcj_test.demo3']  # 要发布的模块

)
