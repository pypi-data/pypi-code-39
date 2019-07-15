#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name = "BlueTest",
    version = "0.3.3",
    author = "liufeng",
    author_email = "xxxx@qq.com",
    description = "",
    long_description = open("README.rst").read(),
    license = "MIT",
    url = "https://github.com",
    packages = ['BlueTest'],
    install_requires = [],
    classifiers = [
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Topic :: Text Processing :: Indexing",
    "Topic :: Utilities",
    "Topic :: Internet",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    ],
)