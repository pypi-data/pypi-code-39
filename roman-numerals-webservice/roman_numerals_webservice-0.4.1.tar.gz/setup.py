#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0', 
    'cherrypy>=18.0.0'
    'requests>=2.22.0'
]

setup_requirements = ['pytest-runner', 'numpy']

test_requirements = ['pytest', 'numpy']

setup(
    author="Thorsten Beier",
    author_email='derthorstenbeier@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A python package for a minimalist webservice to convert roman numerals to araic numerals and vice versa.",
    entry_points={
        'console_scripts': [
            'roman_numerals_webservice=roman_numerals_webservice.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license", 
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='roman_numerals_webservice',
    name='roman_numerals_webservice',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DerThorsten/roman_numerals_webservice',
    version='0.4.1',
    zip_safe=False,
)
