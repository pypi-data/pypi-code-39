# Copyright (c) 2019 Anson Biggs
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdfparse",
    version="2019.5.1",
    author="Anson Biggs",
    author_email="anson@ansonbiggs.com",
    description="A package for reading .bdf files into NumPy arrays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/MisterBiggs/bdf-to-numpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
