# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="gen-repr",
    version="0.2.0",
    author="Peter Morawski",
    author_email="web@peter-morawski.de",
    keywords="make repr auto generate",
    description="Automatically generate the repr of a class with all it's fields",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Peter-Morawski/gen-repr",
    test_suite="tests",
    py_modules=["genrepr"],
    license="MIT License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Widget Sets",
        "Topic :: Utilities",
    ],
)
