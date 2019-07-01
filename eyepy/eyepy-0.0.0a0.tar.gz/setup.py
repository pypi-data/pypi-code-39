import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eyepy",
    version="0.0.0a",
    author="Dillon Gwozdz",
    author_email="dillongwozdz@gmail.com",
    description="Eyetracking Software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dillongwozdz/eyepy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
)