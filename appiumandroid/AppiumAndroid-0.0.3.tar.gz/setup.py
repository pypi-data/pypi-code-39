#!/usr/bin/env python

import setuptools
#
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AppiumAndroid",
    version="0.0.3",
    author="zhenghong",
    author_email="743872668@qq.com",
    description="",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)