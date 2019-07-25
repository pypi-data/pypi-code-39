#!/usr/bin/env python3

# stdlib
import codecs
from os import path

# third-party
from setuptools import setup
from setuptools import find_packages

# local
import alogs


here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'README.rst')


with codecs.open(readme, encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=alogs.__name__,
    version=alogs.__version__,
    description="Custom Logging Module",
    long_description=long_description,
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License"
    ],
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='logging',
    author=alogs.__author__,
    author_email=alogs.__email__,
    url=alogs.__url__,
    download_url="{u}/archive/v{v}.tar.gz".format(u=alogs.__url__,
                                                  v=alogs.__version__),
    packages=find_packages(exclude=['ez_setup', 'examples',
                                    'tests', 'docs', '__pycache__']),
    package_data={},
    platforms='os x, linux, windows'
)
