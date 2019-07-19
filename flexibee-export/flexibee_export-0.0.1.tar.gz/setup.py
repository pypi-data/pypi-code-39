import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flexibee_export",
    version="0.0.1",
    author="Endevel",
    author_email="info@endevel.cz",
    description="FlexiBee xml export package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EndevelCZ/flexibee-export.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)