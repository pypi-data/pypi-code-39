import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metis-utils",
    version="0.0.1",
    author="Cliff Clive",
    author_email="cliff.clive@thisismetis.com",
    description="A collection of utilities for faster data science project development.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thisismetis/metis-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)