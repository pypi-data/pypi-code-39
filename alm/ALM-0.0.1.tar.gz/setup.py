# python setup.py sdist bdist_wheel


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ALM",
    version="0.0.1",
    author="Martin Zhao",
    author_email="martin@pku.edu.cn",
    description="ALM Model in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ActMartin/PyALM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)