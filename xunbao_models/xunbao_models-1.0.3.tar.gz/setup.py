# coding: utf-8
import codecs
import os
import sys
import setuptools

# try:
#     from setuptools import setup
# except:
#     from distutils.core import setup

"""
打包的用的setup必须引入，
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

if sys.version_info < (3, 6):
    sys.exit('Python 3.6 or greater is required.')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst', 'rb') as fp:
    readme = fp.read()

# 版本号，自己随便写
VERSION = "1.0.3"

LICENSE = "MIT"

setup(
    name='xunbao_models',
    version=VERSION,
    description=(
        'xunbaowang数据模型'
    ),
    long_description=readme,
    author='skytotwo',
    author_email='381944069@qq.com',
    maintainer='skytotwo',
    maintainer_email='381944069@qq.com',
    license=LICENSE,
    packages=setuptools.find_packages(),
    platforms=["all"],
    url='http://github.com',
    install_requires=[

    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)