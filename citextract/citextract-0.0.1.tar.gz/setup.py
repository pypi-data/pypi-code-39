import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="citextract",
    version="0.0.1",
    author="Kevin Jacobs",
    author_email="kevin91nl@gmail.com",
    description="CiteXtract - Bringing structure to the papers on ArXiv.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmjjacobs/citextract",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)