#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: jie.hang
# Mail: jie.hang@iluvalar.ai
# Created Time:  2019-5-15 14:17:34
#############################################

from setuptools import setup, find_packages

setup(
    name="tflex",
    version="1.0.0rc0",
    keywords=("pip", "tflex", "EPU", "edge computing"),
    description="An edge inference library on embedded device with EPU designed by iluvatar.ai.",
    long_description="An edge inference library on embedded device that contains Edge EPU coprocessor. It's ideal for prototyping new projects that demand fast on-device inferencing for machine learning models. tflex library provides two command line tools: tflexconverter is provided to convert .pb/.h5 model to .tflex model directly supported on EPU, and tflexviewer is supplied to display the network architecture(.pb and .tflex file are both supported) more intuitively based on advanced tensorboard. That is, when a pre-trained or custom model are prepared, then you can use tflexconverter command to convert the model to EPU format, and deploy the model in your device for inference.",
    license="Iluvatar.ai Licence",

    url="http://www.iluvatar.ai/",
    author="jie.hang",
    author_email="jie.hang@iluvatar.ai",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    setup_requires=['wheel'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "keras >= 2.2.4",
        "numpy >= 1.16.3",
        "traceback2 >= 1.4.0",
        "tensorflow-tflex >= 1.12.1",
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'tflexconverter  = tflex.script.tflexconverter:main',
            'tflexviewer = tflex.script.tflexviewer:main'
        ],
    }
)
