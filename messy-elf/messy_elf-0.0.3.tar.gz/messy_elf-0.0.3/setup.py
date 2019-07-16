#!/usr/bin/env python

import setuptools

install_requires = [
    'requests>=2.13.0',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="messy_elf",
    version="0.0.3",
    author="Nishant Nayudu",
    author_email="nishant.nayudu@gmail.com",
    description="Testing package for Pypi/Pipenv Functions",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nnayudu/messy-elf",
    install_requires=install_requires,
    packages=setuptools.find_packages('messyelf'),
    package_dir={
        '': 'messyelf',
    },
    keywords=[
        'pypi', 'testing'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)