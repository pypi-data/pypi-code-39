#!/usr/bin/env python

from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="graft_cli",
    version="0.0.5",
    entry_points={"console_scripts": ["graft-cli=graft_cli.main:main"]},
    author="nilinswap",
    author_email="nilinswap@gmail.com",
    description="A command line utitily to provide services offered by graftpress( a graft-elm web framework).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amitu/graftpress/",
    packages=find_packages(),
    install_requires=["cookiecutter>=1.6.0"],
)
