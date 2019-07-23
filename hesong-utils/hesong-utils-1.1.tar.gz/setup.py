#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

py_major_minor = '{0[0]}.{0[1]}'.format(sys.version_info)

# Dependencies by version
install_requires = []
if py_major_minor < '3.4':
    install_requires.append('enum34')

# setup configurations
setup(
    name='hesong-utils',
    namespace_packages=['hesong'],
    packages=find_packages('src', exclude=['tests', 'docs']),
    package_dir={'': 'src'},  # tell distutils packages are under src
    url='http://bitbucket.org/hesong-opensource/hesong-python-utils',
    license='BSD',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    description='Hesong Python Utils',
    # Requires-Python version.
    python_requires='>=2.6',
    # Dependencies Declarations
    install_requires=install_requires,
    extras_require={
        'ujson': ['ujson'],
        'yaml': ['PyYAML'],
        'all': ['ujson', 'PyYAML']
    },
    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
    },
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
)
