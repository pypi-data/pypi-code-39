#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install

VERSION = "0.0.1"


def readme():
    with open('README.md') as f:
        return f.read()


class VerifyVersionCommand(install):
    description = "Simple Django PollsApp"


setup(
    name="Kipkoech-polls",
    version=VERSION,
    description="Simple Django Polls app",
    long_description=readme(),
    url="https://github.com/DenisBiwott/PollsApp",
    author="Denis Kipkoech",
    author_email="deniskipkoech@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords='',
    packages=['PollPackage'],
    install_requires=[
        'requests==2.20.0',
    ],
    python_requires='>=3',
)
