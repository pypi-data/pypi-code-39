# -*- coding: utf-8 -*-

# Copyright 2019, Grid.
#
# This source code is licensed under the ReNom Subscription Agreement, version 1.0.
# ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)


import os
import sys
import re
import shutil
import pathlib
import numpy
from setuptools import setup, find_packages, Extension
import distutils.command.build
from Cython.Build import cythonize
from distutils.extension import Extension


if sys.version_info < (3, 4):
    raise RuntimeError('renom_q requires Python3')

DIR = str(pathlib.Path(__file__).resolve().parent)


requires = ["Cython", "numpy", "matplotlib", "scipy"]

setup(
    name="renom_q",
    version="0.2b2",
    packages=['renom_q'],
    description="Machine learning framework for quantum machine learning and quantum optimization",
    long_description="ReNomQ is a machine learning framework for quantum machine learning and quantum optimization. "
                    "http://renom.jp/packages/renomq/index.html",
    author="Grid.Inc",
    license="ReNom Subscription License (https://www.renom.jp/info/license/index.html)",
    url="https://github.com/ReNom-dev-team/ReNomQ",
    include_package_data=True,
    zip_safe=True,
    install_requires=requires,
    classifiers=[
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='ReNom renom ReNomQ renom_q quantum Frameworks'
)
