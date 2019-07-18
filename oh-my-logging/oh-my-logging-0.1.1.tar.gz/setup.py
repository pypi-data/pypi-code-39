#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import io

from setuptools import setup, find_packages


NAME = 'oh-my-logging'
DESCRIPTION = 'Enhancement for logging.'
URL = 'https://github.com/fsjohnhuang/oh-my-logging'
EMAIL = 'fsjohnhuang@hotmail.com'
AUTHOR = 'fsjohnhuang'
PYTHON_REQUIRES = '>=2.7'
VERSION = '0.1.1'
PLATFORMS='any'
REQUIRED = []

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

try:
    with io.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        REQUIRED = f.read().split('\n')[1:]
except FileNotFoundError:
    pass

about = {}
if not VERSION:
    project_slug = NAME.lower().replace('-', '_').replace(' ', '_')
    with io.open(os.path.join(here, project_slug, '__version__.py'), encoding='utf-8') as f:
        exec(f.read(), about)
else:
    about['version'] = VERSION

setup(
    name=NAME,
    version=about['version'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    url=URL,
    platforms=PLATFORMS,
    python_requires=PYTHON_REQUIRES,
    package_dir={'oh_my_logging':'src/oh_my_logging'},    
    packages=find_packages('./src'),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',                
        'Programming Language :: Python :: 3.2',                
        'Programming Language :: Python :: 3.3',        
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    entry_points={
        'console_scripts': [
            'logging=oh_my_logging:main'
        ]
    },
)
