#!/usr/bin/env python

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="messy_elf",
    version="0.0.5",
    author="Nishant Nayudu",
    author_email="nishant.nayudu@gmail.com",
    description="Testing package for Pypi/Pipenv Functions",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nnayudu/messy-elf",
    packages=setuptools.find_packages('messyelf'),
    package_dir={
        '': 'messyelf',
    },
    keywords=[
        'pypi', 'testing'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)