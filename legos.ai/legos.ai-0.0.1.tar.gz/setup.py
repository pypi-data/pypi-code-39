import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setup(
    name="legos.ai",
    version="0.0.1",
    description="A simple framework for fast protopying of Deep Learning researches.",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/quanhua92/legos",
    author="Quan Hua",
    author_email="quanhua92@gmail.com",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["legos"],
    include_package_data=True,
)