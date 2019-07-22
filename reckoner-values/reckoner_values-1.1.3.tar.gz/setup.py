#!/usr/bin/env python
# -- coding: utf-8 --
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print("setup tools required. Please run: "
          "pip install setuptools).")
    sys.exit(1)

setup(name='reckoner_values',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description='Package to find helm values and update autohelm / reckoner files',
      author='Jim Robinson',
      author_email='jscrobinson@gmail.com',
      version="1.1.1",
      license='Apache2.0',
      packages=['reckoner_values'],
      include_package_data=True,
      install_requires=[
            "click==7.0",
            "GitPython>=2.1.11",
            "oyaml>=0.8",
            "coloredlogs>=9.0",
            "semver>=2.8.1",
            "PyYAML>=5.1",
            "awscli>=1.16",
            "boto3>=1.9",
            "jinja2>=1.2",
            "yq>=2.7",
            "urllib3>=1.25",
            "pyhelm>=0.1",
            "kubernetes>=10.0"
      ],
      entry_points=''' #for click integration
          [console_scripts]
          reckoner-values=reckoner_values.cli:cmd
      '''
      )
