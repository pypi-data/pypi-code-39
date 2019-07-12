#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="isss",
    version="1.0",
    author="Romain Lienard",
    author_email="rlienard@fr.ibm.com",
    description="A unofficial library which provides wrappers around IBM Security Secret Server REST APIs. Also compatible with Thycotic Secret Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ibm.com/marketplace/secret-server",
    packages=setuptools.find_packages(),
    scripts=["isss-fw"],
    keywords=["isss","ibm", "thycotic", "secret", "server"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)