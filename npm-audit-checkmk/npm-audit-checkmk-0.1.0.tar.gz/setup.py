#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as handle:
    README = handle.read()

setup(
    name='npm-audit-checkmk',
    version='0.1.0',
    maintainer='Sebastian Wagner',
    maintainer_email='wagner@cert.at',
    python_requires='>=3.4',
    test_suite='tests',
    packages=find_packages(),
    url='https://github.com/certat/npm-audit-check',
    license='AGPLv3',
    description='Creates checkmk local check file for npm audit output.',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Monitoring',
        'Topic :: Security',
    ],
    entry_points={
        'console_scripts': [
            'npm_audit_checkmk = npm_audit_checkmk.__main__:main',
        ],
    },
)
