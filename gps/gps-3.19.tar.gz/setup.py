import io
import os
import re
from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))


with io.open("gps/__init__.py", "rt", encoding="utf8") as f:
    version = eval(re.search(r'__version__ = (.*)', f.read()).group(1))


setup(
    name='gps',
    version=version,
    author='Eric S. Raymond',
    author_email='esr@thyrsus.com',
    description='GPSD client',
    license='BSD',
    url='https://gitlab.com/gpsd/gpsd',
    packages=find_packages(),
    keywords='gsp',
)
