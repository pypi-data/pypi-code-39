import os
import sys
import codecs
import re

import setuptools
from setuptools.config import read_configuration


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup_params = {
    # dynamically generated params
    'version': find_version('cherrypy_ask_sdk', '__init__.py'),
    'install_requires': [
        line.strip() for line in read("requirements.txt").splitlines()
    ],
}

config = read_configuration("setup.cfg")
setup_params = dict(setup_params, **config['metadata'])
setup_params = dict(setup_params, **config['options'])
setuptools.setup(**setup_params)
