import os
import pathlib
from setuptools import setup

setup(
    name="module-resources",
    # TRAVIS_TAG is an empty string in builds, os.getenv default arg misses this
    version=os.getenv('TRAVIS_TAG') or f"0.0.{os.getenv('TRAVIS_BUILD_NUMBER')}",
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
