#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from os import path
import sys


cur_dir = path.abspath(path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(path.join(cur_dir, 'README.md')) as f:
        long_description = f.read()
else:
    with open(path.join(cur_dir, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

requirements = [
    'altair>=2.4.1,<3',
    'Click>=7.0',
    'pandas>=0.24.2',
]

setup_requirements = []

setup(
    author="Matt Chun-Lum",
    description="Turn test results into a Gantt chart",
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'ganttify=ganttify.__main__:main'
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    keywords='ganttify',
    name='ganttify',
    packages=find_packages(include=['ganttify']),
    setup_requires=setup_requirements,
    version='0.2.1',
    zip_safe=False,
)
