'''
Created on Jul 16, 2019
@author: pankajrawat
'''
import setuptools
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdfutil",
    version="0.0.1",
    author="Pankaj Rawat",
    author_email="pankajr141@gmail.com",
    description="Library provides a useful operations over PDF/Image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pankajr141/pdfutil",
    packages=setuptools.find_packages(),
    install_requires=[
        'pdf2jpg==0.0.9'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)