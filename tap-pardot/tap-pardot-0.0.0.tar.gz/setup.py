#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-pardot",
    version="0.0.0",
    description="Singer.io tap for extracting data from the Salesforce Pardot API",
    author="Rangle.io",
    url="https://github.com/rangle/tap-pardot",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_pardot"],
    install_requires=[
        "singer-python==5.5.0",
        "requests==2.21.0",
        "backoff==1.3.2",
        "ratelimit==2.2.1"
    ],
    extras_require={
        'dev': [
            'pylint',
            'autopep8',
            'rope'
        ]
    },
    entry_points="""
    [console_scripts]
    tap-pardot=tap_pardot:main
    """,
    packages=["tap_pardot"],
    package_data={
        "schemas": ["tap_pardot/schemas/*.json"]
    },
    include_package_data=True,
)
