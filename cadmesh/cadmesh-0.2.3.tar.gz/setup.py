import setuptools
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="cadmesh",
    version="0.2.3",
    author="Sebastian Koch",
    author_email="",
    description="Meshing CAD files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skoch9/cadmesh/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    test_suite="test"
)
