from setuptools import setup

__version__ = "0.1.0"

setup(
    name="searchstring",
    version=__version__,
    description="A library for sophisticated parsing search queries.",
    long_description=open("README.rst").read(),
    author="Marek Kochanowski",
    author_email="marek@maisie.dev",
    url="https://github.com/maisie-dev/searchstring",
    packages=["searchstring"],
    include_package_data=True,
    install_requires=["parsimonious>=0.8.1"],
    license="MIT",
    classifiers=(
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ),
)
