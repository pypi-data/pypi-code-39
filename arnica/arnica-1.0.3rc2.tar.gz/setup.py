#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='arnica',
    version='1.0.3-rc.2',
    description='Open Source library CFD toolkit',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='CoopTeam-CERFACS',
    author_email='coop@cerfacs.com',
    url='https://nitrox.cerfacs.fr/open-source/arnica',
    license="CeCILL-B FREE SOFTWARE LICENSE AGREEMENT",
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=['pytest-runner'],
    install_requires=[
        'pytest',
        'pytest-cov',
        'pylint',
        'numpy',
        'scipy',
        'matplotlib',
        'h5py',
        'lxml',
        'pandas']
)
