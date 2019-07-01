#!/usr/bin/env python

from __future__ import with_statement

import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fp:
        return fp.read()

def _get_version_match(content):
    regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(regex, content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def get_version(path):
    return _get_version_match(read_file(path))

setup(
    name='ansimagic',
    version=get_version(os.path.join('ansimagic', '__init__.py')),
    description='Helper for ansi esc sequence',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='color ansi terminal',
    author='A. Shpak',
    author_email='shpaker@gmail.com',
    maintainer='shpaker',
    url='https://github.com/shpaker/ansimagic',
    license='BSD',
    packages=['ansimagic'],
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Terminals',
    ]
)