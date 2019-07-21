#!/usr/bin/env python

import codecs
from setuptools import setup

# Version info -- read without importing
_locals = {}
with open("alabaster/_version.py") as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

# README into long description
with codecs.open("README.rst", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="aioli_sphinx_theme",
    version=version,
    description="Aioli Sphinx theme, based on Alabaster",
    long_description=readme,
    author="Robert Wikman",
    author_email="rbw@vault13.org",
    url="https://alabaster.readthedocs.io",
    modules=["aioli_sphinx_theme"],
    include_package_data=True,
    entry_points={"sphinx.html_themes": ["aioli_sphinx_theme = aioli_sphinx_theme"]},
)
