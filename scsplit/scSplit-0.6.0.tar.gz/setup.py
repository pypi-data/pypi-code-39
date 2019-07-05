import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scSplit",
    version="0.6.0",
    author="Jun Xu",
    author_email="jun.xu@uq.edu.au",
    description="Genotype-free demultiplexing of pooled single-cell RNA-seq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jon-xu/scSplit",
    download_url="https://github.com/jon-xu/scSplit/archive/0.6.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)