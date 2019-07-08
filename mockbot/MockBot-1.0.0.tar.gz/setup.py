#!/usr/bin/python3
from setuptools import setup

setup(
    name='MockBot',
    version='1.0.0',
    description='A Groupme Bot that Mocks a specified user.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dgisolfi/MockBot',
    author='dgisolfi',
    license='MIT',
    packages=['MockBot'],
    install_requires=[
        'spongemock>=0.3.4',
        'flask>=0.12.3',
        'requests>=2.20.0',
        'markdown>=2.6.11',
    ],
    zip_safe=False
)