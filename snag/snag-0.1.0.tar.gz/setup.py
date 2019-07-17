from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="snag",
    version="0.1.0",
    description="A tool to batch-download files from the internet",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Willem Hunt",
    author_email="whunt1@uvm.edu",
    url="https://github.com/willemhuntuvm/snag",
    license="MIT License",
    packages=find_packages(exclude=["tests*"]),
    install_requires=["beautifulsoup4","requests"],
    scripts=["bin/snag"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
