#!/usr/bin/env python

from setuptools import setup, find_packages

import ext_sort

requirements = [
]

test_requirements = [
    'pytest==4.4.1'
]

with open('README.rst', 'r') as file:
    readme = file.read()

setup(
    name=ext_sort.__title__,
    version=ext_sort.__version__,
    description=ext_sort.__description__,
    long_description=readme,
    author=ext_sort.__author__,
    author_email=ext_sort.__email__,
    url=ext_sort.__url__,
    license=ext_sort.__license__,
    keywords=['python3', 'sort', 'external-sort', 'algorithms'],
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
