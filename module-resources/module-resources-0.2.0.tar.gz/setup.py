import os
import pathlib
import pkg_resources
from setuptools import setup

# this script sets the version number in CI builds, and also at install time by the user
VERSION = None
TRAVIS_TAG, TRAVIS_BUILD_NUMBER = map(os.getenv, ('TRAVIS_TAG', 'TRAVIS_BUILD_NUMBER'))
if not TRAVIS_TAG and not TRAVIS_BUILD_NUMBER:
    # not a CI build, user is installing package
    user_installed_version = pkg_resources.require('module-resources')[0].version
    VERSION = user_installed_version
else:
    VERSION = TRAVIS_TAG or f"0.0.{TRAVIS_BUILD_NUMBER}"

setup(
    name="module-resources",
    version=VERSION,
    description="Import non-python files in a project directory as python namedtuple objects.",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/captain-kark/module_resources",
    author="Andrew Yurisich",
    author_email="andrew.yurisich@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["module_resources"],
    extras_require={
        'yaml': ['pyyaml']
    }
)
