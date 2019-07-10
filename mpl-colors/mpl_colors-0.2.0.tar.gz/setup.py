from setuptools import setup
from pathlib import Path


root = Path(__file__).resolve().parent
long_description = (root / "README.md").read_text()


setup(
    name="mpl_colors",
    version="0.2.0",
    packages=["mpl_colors"],
    url="https://github.com/clbarnes/mpl_colors",
    license="MIT",
    author="Chris L. Barnes",
    install_requires=["colour", "numpy", "matplotlib"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    author_email="",
    description="Enums representing named colors available in matplotlib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
)
