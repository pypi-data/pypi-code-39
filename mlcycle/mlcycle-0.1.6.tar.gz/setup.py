import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlcycle",
    version='0.1.6',
    url="http://git01-ifm-min.ad.fh-bielefeld.de/pvserve2/mlcycle",
    author="Cem Basoglu",
    author_email="cem.basoglu@fh-bielefeld.de",
    description="MLCycle client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ]
)
