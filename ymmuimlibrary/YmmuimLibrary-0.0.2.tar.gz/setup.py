# _*_ coding=utf-8 _*_
__author__  = "8034.com"
__date__    = "2019-07-01"

from setuptools import setup, find_packages
import sys
import os
 
from YmmuimLibrary.version import VERSION

__version__ = VERSION

setup(
    name="YmmuimLibrary",
    version = __version__,
    author="goblinintree",
    author_email="goblinintree@126.com",
    description="YmmuimLibrary is a Mobile App testing library for Robot Framework, in Python3",
    long_description=open("README.md",encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    platforms=["all"],
    license="MIT",
    keywords = ['Appium', 'Robot Framework', 'YmmuimLibrary'],
    url="https://pypi.org/project/YmmuimLibrary/#description",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
    install_requires=[
        "robotframework",
    ],
    dependency_links = [
    ],
)