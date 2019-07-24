from pathlib import Path
import setuptools

import lettercase

long_description = Path("README.md").read_text()

setuptools.setup(
    name="lettercase",
    version=lettercase.__version__,
    description="Detection and conversion between letter cases",
    author="Giesela Inc.",
    author_email="team@giesela.dev",

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gieseladev/lettercase",

    packages=setuptools.find_packages(exclude=("tests", "venv")),
    python_requires="~=3.7",
)
