#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'graphene_django>=2.2.0<=2.4.0',
    'graphene-file-upload==1.2.2',
    'sentry-sdk>=0.5.2<=0.10.1',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Alexander Lushnikov",
    author_email='alexander.aka.alegz@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Capture Sentry exceptions in Graphene views",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='GraphQL graphene sentry',
    name='graphene-sentry',
    packages=find_packages(include=['graphene_sentry']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Alegzander/graphene-sentry',
    version='0.4.0',
    zip_safe=False,
)
