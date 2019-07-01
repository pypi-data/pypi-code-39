# -*- encoding: UTF-8 -*-
import os
import sys

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

requires = [
    'setuptools',
    'cx_Oracle',
    'sqlalchemy'
]

setup(
    name='litex.cxpool',
    version='1.1',
    description='Native Oracle Session Pool implementation for SQLAlchemy',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Database :: Front-Ends"
    ],
    author='Michal Wegrzynek',
    author_email='mwegrzynek@litexservice.pl',
    license='BSD like, see http://repoze.org/license.html',
    keywords='cxpool oracle sessionpool sqlalchemy proxy',
    namespace_packages=['litex'],
    packages=['litex.cxpool'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=['pytest']
)
