#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

readme = os.path.join(os.path.dirname(__file__), '..', 'README.md')

with open(readme, 'r') as f:
    long_desc = f.read()

setup_requirements = [
    'setuptools-scm>=3.1.0'
]

requirements = [
    'aiohttp>=3.5.4',
    'netifaces>=0.10.7'
]

setup(
    name='terrycain-metadata-proxy',
    use_scm_version={
        'root': '..',
        'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)$',
        'write_to': 'proxy/metadata_proxy/version.py'
    },
    description='AWS Metadata Proxy',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/terrycain/metadata-proxy/',
    author='Terry Cain',
    author_email='terry@terrys-home.co.uk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: AsyncIO',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='aws metadata proxy',
    packages=find_packages(exclude=['tests', 'docs']),
    setup_requires=setup_requirements,
    install_requires=requirements,
    extras_require={
        'uvloop': ['uvloop>=0.12.2']
    },
    entry_points={
        'console_scripts': [
            'metadata-proxy=metadata_proxy.server:run'
        ]
    }
)
