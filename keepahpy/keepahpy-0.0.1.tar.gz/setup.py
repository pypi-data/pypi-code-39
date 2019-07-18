import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="keepahpy",
    version="0.0.1",
    author="Antoine Daurat",
    author_email="antoine.daurat@pwc.com",
    description="Flask-SDK for Keepah",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.dsnexus.org/keepah/keepah-flask-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)