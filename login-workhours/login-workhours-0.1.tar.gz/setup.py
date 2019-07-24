# -*- coding: utf-8 -*-
import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    with open(filename) as lines:
        lineiter = (line.strip() for line in lines)
        return [line for line in lineiter if line and not line.startswith("#")]


def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding="utf-8") as f:
        content = f.read()
    return content


README = read_file("README.rst")


ENTRY_POINTS = {"console_scripts": ["workhours = workhours:main"]}

setup(
    name="login-workhours",
    version="0.1",
    description="Compute working hours based on login / logouts events.",
    long_description=README,
    license="Custom BSD Beerware",
    classifiers=["Programming Language :: Python :: 3.7"],
    keywords="time-management",
    author="Alexis Métaireau & contributors",
    author_email="alexis@notmyidea.org",
    url="https://framagit.org/almet/workhours",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True,
    zip_safe=False,
    entry_points=ENTRY_POINTS,
)
