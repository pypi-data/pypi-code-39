import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "NssErrorLogger",
    version = "0.0.1",
    author = "Uncertainty.",
    author_email = "tk@uncertainty.cc",
    description = "Error Logger",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
