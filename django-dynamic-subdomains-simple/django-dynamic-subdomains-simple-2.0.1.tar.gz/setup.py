#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-dynamic-subdomains-simple',
    description="Dynamic and static subdomain support for Django.",
    version='2.0.1',

    author="Chris Adkins",
    author_email='c23gooey@gmail.com',
    license='MIT',

    packages=find_packages(),

    install_requires=(
        'Django>=2.2',
    ),
)
