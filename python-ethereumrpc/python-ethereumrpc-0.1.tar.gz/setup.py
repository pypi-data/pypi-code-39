#!/usr/bin/env python
# forked from https://github.com/jgarzik/python-bitcoinrpc
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-ethereumrpc',
    version='0.1',
    description='Enhanced version of python-jsonrpc for use with Ethereum',
    long_description=open('README.md').read(),
    author='Linggih Saputro',
    author_email='<linggih.saputro@sci.ui.ac.id>',
    maintainer='Linggih Saputro',
    maintainer_email='<linggih.saputro@sci.ui.ac.id>',
    url='http://www.github.com/nggih/python-ethereumrpc',
#     packages=['ethereumrpc'],
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)', 'Operating System :: OS Independent'
    ]
)
