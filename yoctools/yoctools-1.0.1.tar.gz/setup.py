#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from codecs import open  # To use a consistent encoding

from setuptools import setup  # Always prefer setuptools over distutils

APP_NAME = 'yoctools'
VERSION = '1.0.1'

settings = dict()


settings.update(
    name=APP_NAME,
    version=VERSION,
    description='YoC tools',
    author='Zhuzhg',
    author_email='zzg@ifnfn.com',
    packages=['yoc'],
    install_requires=['pyyaml>=5.0.0', 'scons>=3.0.0'],
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'toolchain = yoc.toolchain:main',
        ],
    }
)


setup(**settings)
