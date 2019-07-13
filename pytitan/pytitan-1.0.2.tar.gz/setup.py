# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, 'requirements.txt')) as reqs_file:
    REQS = reqs_file.read()

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name='pytitan',
    version='1.0.2',
    packages=find_packages(exclude=["tests"]),
    install_requires=REQS,
    url='http://120.77.169.160:10001/python/pytitan',
    license='BSD',
    author='Ray',
    author_email='csharp2002@hotmail.com',
    description="The computing framework for microservice.",
    long_description=README,
    zip_safe=False,
    platforms='any',
    keywords=['titan', 'microservice', 'ynkg', 'newland'],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Utilities'])
