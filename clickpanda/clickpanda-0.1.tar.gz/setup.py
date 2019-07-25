#!/usr/bin/env python

import versioneer
from os.path import exists
from setuptools import setup


setup(name='clickpanda',
      version='0.1',
      description='Pandas interface for Clickhouse HTTP API',
      url='http://github.com/kszucs/pandahouse',
      maintainer='Dikiy Pes',
      maintainer_email='dikiy.pes@gmail.com',
      license='BSD',
      packages=['clickpanda'],
      tests_require=['pytest'],
      setup_requires=['pytest-runner'],
      install_requires=['pandas', 'requests', 'toolz'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)
