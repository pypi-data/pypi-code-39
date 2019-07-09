#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

readme = 'README.md'
with open(readme) as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(name='corpus-middleware',
      version='0.2.9',
      description='corpus-middleware',
      long_description=long_description,
      install_requires=requirements,
      author='metasota',
      author_email='liuwentao@metasota.ai',
      url='https://metasota.ai/',
      entry_points='''
            [console_scripts]
            corpus-middleware=middleware.command_manage_corpus_file:cli
        ''',
      packages=['middleware',
                'middleware.api',
                'middleware.downloader',
                'middleware.settings',
                'middleware.utils'],
      )
