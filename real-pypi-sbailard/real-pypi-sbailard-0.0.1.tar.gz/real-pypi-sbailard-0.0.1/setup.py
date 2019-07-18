
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="real-pypi-sbailard",
    version="0.0.1",
    author="Sophie Bailard",
    author_email="sophie.bailard1@gmail.com",
    description="Testing useing pypi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)