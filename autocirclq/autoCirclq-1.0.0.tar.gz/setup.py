#!/usr/bin/env python

from distutils.core import setup

setup(name='autoCirclq',
      version='1.0.0',
      description='autoCirclq 是一个编写测试用例后，运行会通过断言结果自动生成报告',
      author='circlq',
      author_email='circlq@qq.com',
      url='https://www.jianshu.com/u/f55907bdfb8e',
      packages=['autoCirclq.common', 'autoCirclq.common.util','autoCirclq.runner'],
     )