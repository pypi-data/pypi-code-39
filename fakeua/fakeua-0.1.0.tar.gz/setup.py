#!/usr/bin/env python3

from setuptools import setup
from pathlib import Path

readme = Path("README.md").read_text()


setup(
    name="fakeua",
    packages=["fakeua"],
    entry_points={
        "console_scripts": [
            "fakeua = fakeua.__main__:main"
        ]
    },
    version="0.1.0",
    license="GPL3",
    description="Python3 module made as a wrapper of fake-useragent.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/fakeua",
    download_url="https://github.com/carlosplanchon/"
        "fakeua/archive/v0.1.0.tar.gz",
    keywords=["fake", "useragent", "networking", "web"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
