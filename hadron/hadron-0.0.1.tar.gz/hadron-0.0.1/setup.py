from codecs import open
from os import path

from setuptools import setup

basedir = path.abspath(path.dirname(__file__))

with open(path.join(basedir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hadron",
    version="0.0.1",
    description="The last validation library you will ever need",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itflex/py-hadron",
    author="iTFLEX Tecnologia Ltda.",
    author_email="dev@itflex.com.br",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="hadron validation",
    packages=["hadron"],
)
