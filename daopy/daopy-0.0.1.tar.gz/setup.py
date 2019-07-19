import pathlib
from setuptools import setup

# the directory containing this file
BASE_DIR = pathlib.Path(__file__).parent

# the text of the README file
README = (BASE_DIR / "README.md").read_text()

setup(
    name="daopy",
    version="0.0.1",
    url="https://github.com/monocongo/daopy",
    license="GPL-3",
    author="James Adams",
    author_email="monocongo@gmail.com",
    description=(
        "This project provides an implementation of the DAO (data access "
        "object) design pattern in Python."
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["daopy"],
    include_package_data=True,
    install_requires=[
        "psycopg2",
        "sqlalchemy",
        "sqlalchemy-utils",
    ],
    tests_require=["pytest"],
    test_suite="tests",
    keywords=(
        "database",
        "DAO",
    ),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
