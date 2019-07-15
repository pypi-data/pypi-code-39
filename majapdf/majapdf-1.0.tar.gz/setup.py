import setuptools
from pathlib import Path

setuptools.setup(
    name="majapdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])

)
