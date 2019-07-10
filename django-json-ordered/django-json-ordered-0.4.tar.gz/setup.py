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
    long_description_content_type='text/markdown',
    author='Rafael Gontijo',
    author_email='rafaelgontijowinter@gmail.com',
    url='https://github.com/rafaelgontijo/django_json_ordered',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.3",
    install_requires=[
        "django >= 1.8.0",
    ],
    include_package_data=True,
)
