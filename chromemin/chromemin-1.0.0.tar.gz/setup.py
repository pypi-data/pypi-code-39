#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'websockets==7.0',
    'aiohttp==3.5.4'
]

setup(
    name='chromemin',
    version='1.0.0',
    description="A Python Package for the Google Chrome Dev Protocol",
    long_description=readme,
    author="mousemin",
    author_email='mousezjf@gmail.com',
    url='https://github.com/mousemin/chromemin',
    packages=find_packages(),
    package_dir={},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='chromemin',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
)