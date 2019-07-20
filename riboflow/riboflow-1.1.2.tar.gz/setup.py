import os,glob
from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="riboflow",
    version="1.1.2",
    author="Ashok Palaniappan, Keshav Aditya R.P, Ramit Bharanikumar",
    author_email="apalania@scbt.sastra.edu, keshavaditya26896@gmail.com, ramitb@rocketmail.com",
    description="Classifying Putative Riboswitch Sequences",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RiboswitchClassifier/riboflow",
    packages=['riboflow'],
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)      