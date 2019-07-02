# -*- coding: utf-8 -*-
"""Setup script for picat_kernel package."""

import glob

DISTNAME = 'picat_kernel'
DESCRIPTION = 'A Picat kernel for Jupyter'
LONG_DESCRIPTION = open('README.md', 'rb').read().decode('utf-8')
MAINTAINER = 'Marcio Minicz'
MAINTAINER_EMAIL = 'marciominicz@gmail.com'
URL = 'https://gitlab.com/minicz/picat_kernel'
LICENSE = 'MPL-2.0'
REQUIRES = ["metakernel", "jupyter"]
INSTALL_REQUIRES = ["metakernel", "jupyter"]
PACKAGES = [DISTNAME]
DATA_FILES = [
    ('share/jupyter/kernels/picat', [
        '%s/kernel.json' % DISTNAME
     ]
    )
]
CLASSIFIERS = """\
Intended Audience :: Science/Research
License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
Operating System :: MacOS
Operating System :: POSIX :: Linux
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Scientific/Engineering
Topic :: Software Development
Topic :: System :: Shells
Framework :: Jupyter
"""

from setuptools import setup

with open('picat_kernel/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break


setup(
    name=DISTNAME,
    version=version,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    packages=PACKAGES,
    data_files=DATA_FILES,
    url=URL,
    download_url=URL,
    license=LICENSE,
    platforms=["Any"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=list(filter(None, CLASSIFIERS.split('\n'))),
    requires=REQUIRES,
    install_requires=INSTALL_REQUIRES
)
