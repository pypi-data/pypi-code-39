import setuptools
from os import path
from io import open
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name = "faciljsondb",
    packages = ["pack"],
    version="0.0.5",
    author="REYMUNDUS",
    author_email="arceleandro2016@gmail.com",
    description="Un paque te encargado de ayudarte a hacer base de datos censillas en json",
    long_description=long_description,
    long_description_content_type='text/markdown', 
    url="https://github.com/reymundus2/facil-json-db",
    keyword=[]
)