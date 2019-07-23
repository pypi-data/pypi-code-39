#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-19 18:52
# @Author  : weihuchao
import os

import setuptools


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setuptools.setup(
    name="django_ricker",
    version="0.0.3",
    author="weihuchao",
    author_email="weihuchao@gmail.com",
    description="django some utils, make it convenient for work. ",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/weihuchao/django_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
