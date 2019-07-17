import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Euclid-FasterCoding",
    version="0.1.0",
    author="FasterCoding",
    author_email="fastercodingtutorial@gmail.com",
    description="Example for the euclidean gcd and extgcd algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FasterCoding/Greatest-Common-Divisor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)