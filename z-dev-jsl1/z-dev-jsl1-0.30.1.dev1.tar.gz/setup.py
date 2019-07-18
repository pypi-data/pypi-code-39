#!/usr/bin/env python3
#
# Copyright (c) 2018 Sébastien RAMAGE
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""
zigate, setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
from distutils.util import convert_path
from os import path

here = path.abspath(path.dirname(__file__))
# Get __version without load zigate module
main_ns = {}
version_path = convert_path('zigate/version.py')
with open(version_path) as version_file:
    exec(version_file.read(), main_ns)
# Setup part
setup(
    name='z-dev-jsl1',
    version=main_ns['__version__'],
    url='https://github.com/jsl-1/',
    author='Jsl-1',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],

    keywords='',
    packages=['zigate'],
    include_package_data=True,

    install_requires=[
        'pyserial',
        'pydispatcher',
        'bottle',
        'RPi.GPIO'
    ],
    extras_require={
        'dev': ['tox'],
        'mqtt': ['paho-mqtt']
    },
    python_requires='>=3',

    project_urls={
        'Source': 'https://github.com/jsl-1/',
    },
    test_suite='tests',
)
