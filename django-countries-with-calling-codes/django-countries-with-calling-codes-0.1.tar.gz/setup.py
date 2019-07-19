#!/usr/bin/env python
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REQUIREMENTS = [
    'Django>=1.11',
    'geoip2>=2.9.0',
]

setup(
    name='django-countries-with-calling-codes',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Django-countries fork with calling codes and geoip2 integration added',
    long_description=README,
    url='https://github.com/rondebu/django-countries-with-calling-codes',
    author='Rondebu Software',
    author_email='info@rondebu.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=REQUIREMENTS,
)
