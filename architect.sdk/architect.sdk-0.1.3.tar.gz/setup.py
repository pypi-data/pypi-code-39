# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='architect.sdk',
      version='0.1.3',
      description='Architect Python SDK',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/architect-team/python-sdk',
      author='architect.io',
      author_email='packages@architect.io',
      license='GPL-3.0',
      packages=['architect.sdk'])
