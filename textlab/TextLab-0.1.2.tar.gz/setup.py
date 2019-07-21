# -*- coding: utf-8 -*-
# TextAnalytics (textanalytics)

import setuptools

import textlab as package
VERSION = package.__version__
DISTNAME = package.__distname__
DESCRIPTION = package.__description__
URL = package.__url__

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
	
setuptools.setup(
	name=DISTNAME,
	version=VERSION,
    author="Sumudu Tennakoon",
    #author_email="author@example.com",
	description=DESCRIPTION,
	license="Apache License Version 2.0",
	long_description=LONG_DESCRIPTION,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	install_requires=["numpy", "scipy", "matplotlib", "pandas", "pymltoolkit", "beautifulsoup4"],
	url=URL,
    classifiers=["Development Status :: 3 - Alpha",
				"Environment :: Console",
				"Intended Audience :: Science/Research",
				"Intended Audience :: Education",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: Apache Software License",
				"Operating System :: OS Independent",
				"Programming Language :: Python",
				"Operating System :: OS Independent",
				"Topic :: Scientific/Engineering",
				"Topic :: Software Development"
				],
)
