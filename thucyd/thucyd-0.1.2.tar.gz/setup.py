#!/usr/bin/env python

# Original from
#  https://raw.githubusercontent.com/ionelmc/python-nameless/purepython/setup.py

# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    # id
    name='thucyd',
    url='https://gitlab.com/thucyd-dev/thucyd',

    # key meta
    version='0.1.2',
    license='Apache License 2.0',
    description="""Scientific library for realtime signal processing and eigenanalysis of evolving systems.""",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',

    # authorship and related
    author='Jay Damask',
    author_email='jaydamask@buell-lane-press.co',

    # project meta
    project_urls={
        'Documentation': 'https://gitlab.com/thucyd-dev/thucyd/',
        'Changelog': 'https://gitlab.com/thucyd-dev/thucyd/',
        'Issue Tracker': 'https://gitlab.com/thucyd-dev/thucyd/issues',
    },
    keywords=[
        'signal processing', 'eigen'
    ],
    classifiers=[
        # ref to https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering'
    ],

    # packaging details
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],

    # requirements and dependencies
    python_requires='>=3.5',
    install_requires=[
        'numpy>=1.14'
    ],
    extras_require={},
)
