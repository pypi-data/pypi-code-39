#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(
    name='cameras-cli',
    version='1.0',
    description='Cameras CLI',
    author='Omar Diaz',
    author_email='zcool2005@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'requests',
      'netifaces',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'cameras=cameras_cli:main',
        ]
    },
)