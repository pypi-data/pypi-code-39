import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RateMyProfessorPyAPI",
    version="1.1.0",
    author="Alex Lu",
    author_email="yiyangl6@asu.edu",
    description="An API written by python to provide support for gathering info from RMP website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remiliacn/RateMyProfessorPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)