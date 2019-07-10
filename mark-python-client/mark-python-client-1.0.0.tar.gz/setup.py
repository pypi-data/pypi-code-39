import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mark-python-client",
    version="1.0.0",
    author="Georgi Nikolov",
    author_email="contact@cylab.be",
    description="A script to connect to the MARK server via python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cylab.be/cylab/mark-python-client",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
