import setuptools
from pathlib import Path

setuptools.setup(
    name = "manishpdf",
    version = 1.0,
    long_description = Path('ReadMe.md').read_text(),
    packages = setuptools.find_packages(exclude = ["tests","data"])
)

