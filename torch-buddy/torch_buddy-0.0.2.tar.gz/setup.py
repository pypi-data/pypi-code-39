from __future__ import absolute_import
import sys
import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torch_buddy",
    version="0.0.2",
    author="鲲(China)",
    author_email="972775099@qq.com",
    description="pytorch toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NickYi1990/torch_buddy",
    install_requires=["pandas-summary>=0.0.5"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
