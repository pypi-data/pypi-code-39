#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from MyLibrary.version import VERSION

requirements = [
    
]

test_requirements = [

]

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: Public Domain
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(
    name='xwfintech-robotframework-common',
    version=VERSION,
    description="xwfintech-robotframework-common is a Robot Framework test library in xwfnitech",
    author="bryanhou",
    author_email='',
    url='https://github.com/houfy-github/robotframework-redislibrary.git',
    packages=[
        'MyLibrary'
    ],
    package_dir={'xwfintech-robotframework-common':
                 'MyLibrary'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='robotframework commonlibrary in xwfintech',
    classifiers=CLASSIFIERS.splitlines(),
    test_suite='tests',
    tests_require=test_requirements
)
