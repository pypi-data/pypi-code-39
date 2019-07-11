"""
https://realpython.com/pypi-publish-python-package/
"""

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent
pypi_package = "tensorflow-ops"

# The text of the README file
# README = (HERE / "README.md").read_text()
README = pypi_package

# This call to setup() does all the work
setup(
    name=pypi_package,
    version="0.0.0",
    description=pypi_package,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SpikingNeurons",
    author=pypi_package,
    author_email="praveenneuron@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    # packages=["reader"],
    # include_package_data=True,
    # install_requires=["feedparser", "html2text"],
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)