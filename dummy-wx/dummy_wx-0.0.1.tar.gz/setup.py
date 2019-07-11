#!/usr/bin/env python
"""Setup script"""

from setuptools import setup, find_packages
setup(
    author="Dominic Davis-Foster",
    author_email="dominic@davis-foster.co.uk",
    description="This module does nothing",
    license="GPLv3",
    long_description="This module does nothing, but us useful when trying to build documentation for modules that require wxpython.",
    name= "dummy_wx",
    packages=find_packages(),
    version="0.0.1",
    )
