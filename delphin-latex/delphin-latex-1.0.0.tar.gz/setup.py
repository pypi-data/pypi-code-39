#!/usr/bin/env python3

import os
from setuptools import setup

base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='delphin-latex',
    version='1.0.0',
    description='LaTeX exporters for DELPH-IN data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/delph-in/delphin-latex',
    author='Michael Wayne Goodman',
    author_email='goodman.m.w@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
    keywords='latex delph-in linguistics',
    packages=['delphin.codecs'],
    install_requires=[
        'pydelphin >= 1.0.0',
    ],
)
