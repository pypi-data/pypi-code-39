#!/usr/bin/env python

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='PLTable',
    version='1.0.0',
    license='BSD (3 clause)',
    description='Python library for easily displaying tabular data in a visually appealing ASCII table format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luke Maurits',
    author_email='luke@maurits.id.au',
    maintainer='Plato Mavropoulos',
    url='https://github.com/platomav/PLTable',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing'
    ],
)