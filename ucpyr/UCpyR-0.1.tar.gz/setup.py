import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UCpyR",
    version="0.1",
    author="Matthew Leighton",
    author_email="Matthew.Leighton@Dal.ca",
    description="A package implementing the UCPR algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://acceleratedresearch.ca",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)