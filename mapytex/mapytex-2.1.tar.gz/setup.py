#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='mapytex',
    version='2.1',
    description='Computing like a student',
    author='Benjamin Bertrand',
    author_email='programming@opytex.org',
    url='http://git.opytex.org/lafrite/Mapytex',
    #packages=['mapytex'],
    packages=find_packages(),
    include_package_data = True,
    install_requires=[
        'multipledispatch',
        'tabulate',
    ],
    )
