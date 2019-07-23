"""
setup.py is configuration information for this PyPI project.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="x3d",
    version="0.0.1",
    author="Don Brutzman",
    author_email="brutzman@nps.edu",
    description="Package support for Extensible 3D (X3D) Graphics International Standard (IS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.web3d.org/x3d/stylesheets/python/x3d.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
