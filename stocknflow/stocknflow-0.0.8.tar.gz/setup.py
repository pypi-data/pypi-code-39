# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
#import os
#if os.environ.get('CI_COMMIT_TAG'):
#    version = os.environ['CI_COMMIT_TAG']
#else:
#    version = os.environ['CI_JOB_ID']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stocknflow",
    version="0.0.8",
    author="Julien Jamme",
    author_email="julien.jamme@protonmail.com",
    maintainer="Julien Jamme",
    description="Stocks and flows maps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mrteste/stocknflow",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: OS Independent",
    ],
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    license = 'GPL3',
    keywords="map stocks proportionnal circles flows",
    install_requires = ['pandas','numpy','geopandas'],
    zip_safe=False,
    package_data={
        'stocknflow': ['data/*.csv']
    }
)
