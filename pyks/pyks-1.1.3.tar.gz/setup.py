from setuptools import setup, find_packages
from version import find_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name = 'pyks',
        author = 'Jiaxiang Li',
        author_email = 'alex.lijiaxiang@foxmail.com',
        description = 'Calculate KS for models',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/JiaxiangBU/pyks",
        license = 'MIT',
        version = find_version('pyks', '__init__.py'),
        packages = find_packages(),
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ]
     )
