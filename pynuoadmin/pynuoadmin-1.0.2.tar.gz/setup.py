#!/usr/bin/env python
# (C) Copyright NuoDB, Inc. 2018  All Rights Reserved.

"""
Setup script for pynuoadmin package. This can be installed using pip as
follows:

    pip install "$NUODB_HOME/drivers/pynuoadmin"

To install with autocomplete dependency:

    pip install "$NUODB_HOME/drivers/pynuoadmin[completion]"

"""

import os
from setuptools import setup

readme = os.path.join(os.path.dirname(__file__), 'README.rst')

metadata = dict(
    name='pynuoadmin',
    version='1.0.2',
    url='https://nuodb.com',
    author='NuoDB',
    author_email='info@nuodb.com',
    license='BSD License',
    description='Python management interface for NuoDB',
    long_description=open(readme).read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: SQL',
        'Topic :: Database',
    ],
    py_modules=['nuodb_cli', 'nuodb_mgmt'],
    install_requires=['requests>=2.8.1,<3.0.0', 'pynuodb>=2.4.0'],
    extras_require=dict(completion='argcomplete>=1.9.0,<2.0.0'),
)

if __name__ == '__main__':
    setup(**metadata)
