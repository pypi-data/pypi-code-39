#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Pmw',
    'pprint',
    'seamm>=0.1',
    'seamm_util>=0.1',
    'seamm_widgets',
]

setup_requirements = [
    'pytest-runner',
    # TODO(emarinri): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='cassandra_step',
    version='0.2.1',
    description="Cassandra is a Monte Carlo molecular simulation package.",
    long_description=readme + '\n\n' + history,
    author="Eliseo Marin-Rimoldi",
    author_email='meliseo@vt.edu',
    url='https://github.com/emarinri/cassandra_step',
    packages=find_packages(include=['cassandra_step']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='cassandra_step',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
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
    entry_points={
        'org.molssi.seamm': [
            'Cassandra = cassandra_step:CassandraStep',
        ],
        'org.molssi.seamm.tk': [
            'Cassandra = cassandra_step:CassandraStep',
        ],
    }
)
