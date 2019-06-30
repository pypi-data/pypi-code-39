#/usr/bin/env python
# coding: utf8
from setuptools import setup, find_packages
from filecoin import version

setup(
    name='filecoin',
    version=version,
    description='filecoin',
    include_package_data=True,
    packages=find_packages(),

    install_requires = [
        'xserver',
    ],

    platforms = 'linux',
)