# -*- coding: utf-8 -*-
#!/usr/bin/env python

from io import open

from setuptools import find_packages, setup

from django_json_ordered.meta import VERSION

setup(
    name='django-json-ordered',
    version=str(VERSION),
    description="It's an ordered json field",
    long_description=open('README.md', encoding='utf-8').read(),
    author='Rafael Gontijo',
    author_email='rafaelgontijowinter@gmail.com',
    url='https://github.com/rafaelgontijo/django-json-ordered',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)