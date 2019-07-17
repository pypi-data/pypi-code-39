#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from setuptools import find_packages



install_requires = [
    'pycryptodome==3.7.3',
    'requests',
    'flask',
    'flask_cors',
    'flask_restful',
    'bs4',
    'openpyxl',
    'pandas',
    'xlrd',
    'flask_sqlalchemy',
    'pyDes',

]

excluded=('pysubway.gitignore',)

setup(
    name='pysubway',
    version='0.0.26',
    author='kougazhang',
    author_email='kougazhang@gmail.com',
    url='https://github.com/kougazhang',
    description='build on flask',
    packages=find_packages(exclude=excluded),
    install_requires=install_requires,
    include_package_data=True
)
