#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup, find_packages


def get_version(*file_paths):
    """Retrieves the version from populate/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("populate", "__init__.py")

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='lib-exo-populator',
    version=version,
    description="""Generic populate models in django from YAML files""",
    long_description=readme + '\n\n' + history,
    author='Tomas Garzon',
    author_email='tomas@openexo.com',
    url='https://github.com/exolever/lib-exo-populator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'singleton-decorator>=1.0.0',
        'stringcase>=1.2.0',
    ],
    license="BSD",
    zip_safe=False,
    keywords='lib-exo-populator',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
)
