# coding: utf-8

"""
Haven Money API
Generated through Open API
"""

from setuptools import setup, find_packages  # noqa: H301

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "haven-client"
VERSION = "0.0.1"

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Haven API",
    author_email="emarx@havenmoney.com",
    url="https://haven.dev",
    keywords=["Haven API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
