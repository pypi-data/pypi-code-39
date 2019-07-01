# Copyright 2019 Kakao Corp
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from setuptools import setup, find_packages


setup(
    name='resourcify',
    version='0.2.3',
    license='MIT License',
    platforms='Linux',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),

    install_requires=['requests', 'python-forge'],

    package_data={
        '': ['*.rst'],
    },

    author='Yang Youseok',
    author_email='ileixe@gmail.com',
    description='Resource library to make ReST client easy',
    long_description=open('README.rst').read(),
    keywords='http rest client',
    url='http://github.com/Xeite/resourcify',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ]
)
