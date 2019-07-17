from setuptools import find_packages, setup
import os

__project__ = "drcompare"
__version__ = "2.2.0"
__description__ = "a Python module to compare the images given in the input CSV file"
__packages__ = [ 'drcompare' ]
__author__ = "Ravjot Singh"
__author_email__ = "ravjotsingh9@yahoo.com"
__requires__ = [ 'matplotlib', 'scipy', 'Pillow', 'scikit-image', 'coverage' ]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    include_package_data=True,
    author = __author__,
    author_email = __author_email__,
    install_requires = __requires__,
)
