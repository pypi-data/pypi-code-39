#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path

from setuptools import setup, find_packages
import country_dialcode
import os
import re


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'(\s*git)|(\s*hg)', line):
            pass
        else:
            requirements.append(line)
    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-country-dialcode-sb',
    version=country_dialcode.__version__,
    description='Django Application providing Dialcode and Countries code',
    long_description=README,
    long_description_content_type='text/x-rst',
    author='Belaid Arezqui',
    author_email='areski@gmail.com',
    url='http://github.com/Star2Billing/django-country-dialcode',
    zip_safe=False,
    packages=find_packages(exclude=["tests", "docs"]),
    package_data={
        "": [
            "fixtures/*",
        ]
    },
    #install_requires=parse_requirements('requirements.txt'),
    # dependency_links=parse_dependency_links('requirements.txt'),
    test_suite='country_dialcode.tests.runtests',
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
