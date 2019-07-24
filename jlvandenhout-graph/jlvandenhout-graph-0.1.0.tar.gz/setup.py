from setuptools import setup


with open("README.md") as f:
    long_description = f.read()


setup(
    name="jlvandenhout-graph",
    version="0.1.0",
    author="J.L. van den Hout",
    packages=["jlvandenhout.graph"],
    description="This package provides a simple graph implementation for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jlvandenhout/graph",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
