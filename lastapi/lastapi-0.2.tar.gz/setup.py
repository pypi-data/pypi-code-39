import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
  long_description = fh.read()
setup(
  name='lastapi',
  version='0.2',
  scripts=['lapi'],
  author="raynix",
  author_email="raynix@gmail.com",
  description="REST API defined as YAML and invoked with lastapi.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/raynix/lastapi",
  packages=['lastapi'],
  package_dir={ 'lastapi': 'lastapi' },
  package_data= { 'lastapi': ['schemas/*.yaml'] },
  classifiers=[
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    "Operating System :: OS Independent",
  ],
)
