#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='py-solc-ast',
    version='0.1.2',
    description="""A tool for exploring the abstrax syntrax tree generated by solc.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ben Hauser',
    author_email='b.hauser@zerolaw.tech',
    url='https://github.com/iamdefinitelyahuman/py-solc-ast',
    include_package_data=True,
    py_modules=['solcast'],
    setup_requires=[],
    python_requires='>=3.5, <4',
    install_requires=[
    ],
    license="MIT",
    zip_safe=False,
    keywords='ethereum solidity solc',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
