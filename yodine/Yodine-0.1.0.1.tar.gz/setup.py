# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="Yodine",
    version="0.1.0.1",
    description="",
    license="MIT",
    author="Gustavo6046",
    packages=find_packages(),
    install_requires=['yodine_data>=0.1.0'] + [r for r in open('requirements.txt').read().split('\n') if r],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ]
)
