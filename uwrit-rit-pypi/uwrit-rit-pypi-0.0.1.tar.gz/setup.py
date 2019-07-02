import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

LICENSE = "BSD 3-Clause License"

setuptools.setup(
    name="uwrit-rit-pypi",
    version="0.0.1",
    author="UW Med Research IT",
    author_email="rithelp@uw.edu",
    description="A simple UW package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uwrit/rit-pypi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
