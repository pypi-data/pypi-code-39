import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitcoin_xyz",
    version="0.0.1",
    author="alphajon",
    author_email="alphajon@126.com",
    description="This is a bitcoin tools package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sincatgit/bitcoin_xyz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)