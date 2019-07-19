# Copyright 2019 Cochlear.ai Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

import io
import os.path

install_requires = [
    'grpcio==1.20.1',
    'grpcio-tools==1.20.1',
    'protobuf==3.7.1',
    'six==1.12.0',
    'pyaudio==0.2.11',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cochl-sense',
    version='1.0.0b2',
    author='Cochlear.ai',
    author_email='support@cochlear.ai',
    description='Python Package for Cochlear.ai sense API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cochlearai/sense-python',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
        ],
    },
    license='Apache 2.0',
    keywords='Cochlear.ai sense client',
    classifiers=(
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ),
)
