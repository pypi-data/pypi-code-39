import setuptools
from pathlib import Path

setuptools.setup(
    name="random-num-py",
    version=1.0,
    long_description=Path("README.txt").read_text(),
    packages=setuptools.find_packages(exclude=['README.md', 'data'])
)
