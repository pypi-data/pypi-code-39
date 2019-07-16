#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sceptre import __version__
from setuptools import setup, find_packages
from os import path

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as history_file:
    history = history_file.read()

install_requirements = [
    "boto3>=1.3,<2.0",
    "PyYaml>=5.1,<6.0",
    "Jinja2>=2.8,<3",
    "packaging==16.8",
    "six>=1.11.0,<2.0.0",
    "networkx==2.1",
]

test_requirements = [
    "pytest>=3.2",
    "troposphere>=2.0.0",
    "moto==1.3.8",
    "mock==2.0.0",
    "behave==1.2.5",
    "freezegun==0.3.12",
    "sceptre-aws-stackoutput-external-resolver==1.0.0",
    "sceptre-aws-stackoutput-resolver==1.0.0"
]

setup_requirements = [
    "pytest-runner>=3"
]

setup(
    name="sceptre-core",
    version=__version__,
    description="Cloud Provisioning Tool",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Cloudreach",
    author_email="sceptre@cloudreach.com",
    license='Apache2',
    url="https://github.com/cloudreach/sceptre",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={
        "sceptre": "sceptre"
    },
    py_modules=["sceptre"],
    data_files=[
        (path.join("sceptre", "stack_policies"), [
            path.join("sceptre", "stack_policies", "lock.json"),
            path.join("sceptre", "stack_policies", "unlock.json")
        ])
    ],
    include_package_data=True,
    zip_safe=False,
    keywords="sceptre",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    test_suite="tests",
    install_requires=install_requirements,
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    extras_require={
        "test": test_requirements
    }
)
