import setuptools
import sys

with open("README.md", 'r') as fh:
    long_description = fh.read()

build_number = sys.argv[1]

setuptools.setup(
    name='bqmigratrr',
    version_command='git describe',
    scripts=["bin/bqmigratrr"],
    author='nick sharp',
    author_email="nick.sharp@urban.co",
    description="Big query schema migration tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urbanmassage/bqmigratrr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
