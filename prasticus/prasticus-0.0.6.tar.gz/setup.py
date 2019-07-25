#!/usr/bin/env python3
# -*-coding: utf8-*-

from setuptools import setup, find_packages
import os
import sys

NAME = 'prasticus'
DESC = 'Catchall module extensible by plugins'
with open("README.md", "r") as fh:
    long_description = fh.read()

setup (
    name = NAME,
    description="Projet {}: {}.".format(NAME, DESC.strip()),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Eric Ringeisen',
    version = '0.0.6',
    author_email="", # Removed.
    url="https://sourceforge.net/projects/prasticus/",
    #package_data = {'': ['*.xml']},
    #zip_safe = True
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=["{}.egg-info".format(NAME)]),
    scripts=[
        # os.path.join('src', NAME, 'script', NAME),
    ],
    entry_points={
        # Install a script as "foo-bar"
        #'console_scripts': [
        #    'foo-bar = prasticus.foobar:main',
        #],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
