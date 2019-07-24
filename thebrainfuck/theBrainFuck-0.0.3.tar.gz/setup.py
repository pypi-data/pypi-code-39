#!/usr/bin/env python
# coding: utf-8

from setuptools import setup,find_packages

setup(
    name='theBrainFuck',
    version='0.0.3',
    author='ZhouYihang',
    author_email='chk18351887132@gmail.com',
    #url='www.google.com',
    description=u'My Own Machine Learning Packages',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=[
        "scipy",
        "numpy",
        "pandas",
        "matplotlib",
        "sklearn",
        "xgboost",
        "lightgbm",
        "catboost"
    ],
    install_requires=[
        "scipy",
        "numpy",
        "pandas",
        "matplotlib",
        "sklearn"
    ]
)