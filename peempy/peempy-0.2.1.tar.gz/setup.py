#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path
import os

version = "0.2.1"

if __name__ == '__main__':
    # Provide static information in setup.json
    # such that it can be discovered automatically

    # Check if in a CI environment
    is_tagged = False
    if os.environ.get('CI_COMMIT_TAG'):
        ci_version = os.environ['CI_COMMIT_TAG']
        is_tagged = True
    elif os.environ.get('CI_JOB_ID'):
        ci_version = os.environ['CI_JOB_ID']
    else:
        # Note in CI
        ci_version = None

    # If in a CI environment, set the version accordingly
    if ci_version:
        # If this a release, check the consistency
        if is_tagged:
            assert ci_version == version, 'Inonsistency between versions'
        else:
            version = ci_version

    README_PATH = path.join(path.dirname(__file__), "README.md")

    with open(README_PATH) as f:
        long_desc = f.read()
    setup(packages=find_packages(),
          name="peempy",
          author="Bonan Zhu",
          author_email="bon.zhu@protonmail.com",
          python_requires='>=3.5',
          version=version,
          classifiers=[
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.5",
              "Programming Language :: Python :: 3.6",
              "Programming Language :: Python :: 3.7",
              "Development Status :: 5 - Production/Stable"
          ],
          description="Python tool for processing XMCD PEEM data",
          url="https://gitlab.com/bz1/peempy",
          license="MIT License",
          long_description_content_type='text/markdown',
          long_description=long_desc,
          entry_points={
              "console_scripts": [
                  "peempy_ob=peempy.peembatch:main",
                  "peempy=peempy.cmdline:peemcli",
                  "peemdata=peempy.datawatcher:main"
              ]
          },
          install_requires=[
              "matplotlib", "colorcet", "scikit-image", "tqdm", "scipy",
              "numpy", "click", "threadpoolctl==1.0.0"
          ],
          extras_require={
              'testing': ['pytest'],
              "pre-commit": [
                  "pre-commit",
                  "yapf",
              ]
          })
