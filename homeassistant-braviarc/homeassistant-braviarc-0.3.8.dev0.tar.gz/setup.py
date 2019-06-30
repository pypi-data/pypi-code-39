# pylint: disable=invalid-name, exec-used
"""Setup braviarc package."""
from __future__ import absolute_import
import sys
import os
from setuptools import setup, find_packages
# import subprocess
sys.path.insert(0, '.')

CURRENT_DIR = os.path.dirname(__file__)

# to deploy to pip, please use
# make pythonpack
# python setup.py register sdist upload
# and be sure to test it firstly using "python setup.py register sdist upload -r pypitest"
setup(name='homeassistant-braviarc',
      # version=open(os.path.join(CURRENT_DIR, 'xgboost/VERSION')).read().strip(),
      version='0.3.8.dev0',
      # long_description_content_type='text/markdown',
      # long_description=open(os.path.join(CURRENT_DIR, 'README.md')).read(),
      description='This package is a temporary solution to update braviarc.',
      install_requires=['requests'],
      maintainer='Antonio Parraga',
      maintainer_email='antonio@parraga.es',
      zip_safe=False,
      packages=find_packages(),
      include_package_data=True,
      url='https://github.com/aparraga/braviarc.git')
