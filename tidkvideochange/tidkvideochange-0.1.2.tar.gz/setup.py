#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 5):
    print('TIDKVideoChange requires at least Python 3.5 to run.')
    sys.exit(1)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'tqdm', 'six', 'lmdb', 'numpy', 'matplotlib', 'pillow', 'importlib_resources', 'opencv-python']

setup_requirements = []

test_requirements = ['torch', 'torchvision']
if sys.version_info >= (3, 7):
    test_requirements += ['tensorflow==1.14.0']
else:
    test_requirements += ['tensorflow==1.12.0']

setup(
    author="Dominik Huss",
    author_email='dhuss@tidk.pl',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Custom modification of VideoText, incorporating pyscenedetect and batching frames.",
    entry_points={
        'console_scripts': [
            'tidkvideochange=tidkvideochange.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tidkvideochange',
    name='tidkvideochange',
    packages=['tidkvideochange',
              'tidkvideochange.crnnpytorch',
              'tidkvideochange.weights'],
    package_data={'tidkvideochange': ['weights/*.pth', 'weights/*.pb']},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DominikHuss/tidkvideochange',
    version='0.1.2',
    zip_safe=False,
)
