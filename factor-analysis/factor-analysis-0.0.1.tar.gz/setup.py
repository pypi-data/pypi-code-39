import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="factor-analysis",
    version="0.0.1",
    author="Aswin Vijayakumar",
    author_email="aswinkv28@gmail.com",
    description="Package to conduct factor analysis on data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avkpy/factor-analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)