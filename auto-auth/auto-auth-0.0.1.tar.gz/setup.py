import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto-auth",
    version="0.0.1",
    author="ggang.liu",
    author_email="ggang.liu@gmail.com",
    description="Using to authenticate automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/auto-then",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)