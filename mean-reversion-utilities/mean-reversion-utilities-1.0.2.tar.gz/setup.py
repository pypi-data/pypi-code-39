# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:37:52 2019

@author: Administrator
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setuptools.setup(
    name="mean-reversion-utilities",
    version="1.0.2",
    description="Time Series mean reversion utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gjlr2000/MeanReversionUtilities.git",
    author="Gerardo Lemus",
    author_email="gerardo@alum.mit.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=["MeanReversionUtilities"],
    include_package_data=True,
    install_requires=["johansen"],

)