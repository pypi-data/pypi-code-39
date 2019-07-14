#!/usr/bin/env python
# encoding: utf-8

"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os
from setuptools import setup, find_packages


def get_long_description():
    """Return readme description"""
    with open('README.md') as fp:
        return fp.read()


def get_version():
    """Return the version of the package"""
    with open(os.path.join('.', 'VERSION')) as fp:
        return fp.read().strip()


setup(
    name='sftputil',
    version=get_version(),
    description='High-level SFTP client library.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Romain TAPREST',
    author_email='romain@taprest.fr',
    url='https://github.com/RomainTT/sftputil',
    packages=find_packages('src'),
    data_files=[('.', ['VERSION'])],
    install_requires=['paramiko'],
    tests_require=['pytest'],
    license="MPL-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
)
