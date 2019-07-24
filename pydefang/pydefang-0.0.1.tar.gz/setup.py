#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

import defang

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = 'pydefang',
        python_requires='>=3',
        version = defang.__version__,
        author = 'Yonathan Klijnsma',
        author_email = 'admin@0x3a.com',
        url = 'https://github.com/0x3a/pydefang',
        packages=find_packages(),
        include_package_data=True,
        description = 'A defang/refang utility written in Python.',
        long_description=read('README.md'),
        long_description_content_type='text/markdown',
        entry_points={
            'console_scripts': [
                'defang=defang:client.defang',
                'refang=defang:client.refang',
            ],
        },
        zip_safe=False,
     )
