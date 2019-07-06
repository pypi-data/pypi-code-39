#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="subshare",
        version="1.0.2",
        author="SimplySublime",
        author_email="sublime@atriox.io",
        description="Linux ShareX alternitve",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/simplysublimee/subShare",
        packages=["bootstrap"],
        include_package_data=True,
        entry_points={
            "console_scripts": [
                "bootstrap=bootstrap.subshare:main",
                ]
            },
        install_requires=[
            "requests",
            "mypolr",
            "pyperclip",
            "click",
            "pyocclient",
            ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        
        )
