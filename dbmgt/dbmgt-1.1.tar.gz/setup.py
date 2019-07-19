#!/usr/bin/env python
#coding: utf-8
from setuptools import setup,find_packages
setup(
    name = 'dbmgt',
    version = '1.1',
    keywords = ('bee', 'egg'),
    description = 'mysql management package',
    license = 'MIT License',
    python_requires='>=3.5, <=3.8',

    url = 'http://blog.swcloud.top',
    author = 'sunway',
    author_email = 'sw1022@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['mysqlclient'],
)
