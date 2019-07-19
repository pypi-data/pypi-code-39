#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pillow',
    'seamm_util',
    'packaging',
    'pprint',
]
# 'rdkit' must be installed by hand using conda

setup_requirements = [
    # 'pytest-runner',
    # TODO(paulsaxe): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='seamm_ff_util',
    version='0.2.1',
    description=("The SEAMM Forcefield utilities read and write forcefields, "
                 "assigns them to molecules, and creates energy expressions."),
    long_description=readme + '\n\n' + history,
    author="Paul Saxe",
    author_email='psaxe@molssi.org',
    url='https://github.com/molssi-seam/seamm_ff_util',
    packages=find_packages(include=['seamm_ff_util']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='seamm_ff_util',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
