#!/usr/bin/env python3
import os
import pyinstinct
from pyinstinct import __version__, __description__, __author__, __email__, __license__
from setuptools import setup, find_packages

pkg_name = 'pyinstinct'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

s = setup(
	name=pkg_name,
	version=__version__,
	license=__license__,
	description=__description__,
	long_description=read("README.md"),
	long_description_content_type='text/markdown',
	keywords="security,scanner",
	url='https://github.com/prahladyeri/pyinstinct',
	packages=find_packages(),
	include_package_data=True,
	entry_points={
		"console_scripts": [
			"pyinstinct = pyinstinct.pyinstinct:main",
		],
	},
	install_requires=[],
	python_requires = ">= 3.4",
	author=__author__,
	author_email=__email__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	)
