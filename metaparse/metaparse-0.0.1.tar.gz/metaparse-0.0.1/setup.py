# Copyright (c) 2018 WeFindX Foundation, CLG.
# All Rights Reserved.

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='metaparse',
    version='0.0.1',
    description='A utility to extract world models of information sources.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/wefindx/metaparse',
    author='Mindey',
    author_email='mindey@qq.com',
    license='ASK FOR PERMISSIONS',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
