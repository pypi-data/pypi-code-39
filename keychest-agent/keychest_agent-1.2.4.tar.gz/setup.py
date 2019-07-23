#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys
import subprocess

import pkg_resources
from setuptools import setup
from setuptools import find_packages

VERSION = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Please update tox.ini when modifying dependency version requirements
install_requires = [
    'requests',
    'setuptools>=1.0',
    'logbook',
    'dnspython',
    'ldap3',
    'psutil'
]

if sys.platform != 'darwin':
    pass
if sys.version_info < (3, 6):
    sys.stderr.write("Python 2 and Python 3.5 or lower are not supported")
    exit(-1)

# crate a git_version file
# noinspection PyBroadException
try:
    git_version_b = subprocess.check_output(['git', 'describe', '--always'], stderr=subprocess.DEVNULL)  # returns bytes
    VERSION = git_version_b.decode().strip()

    with open('./keychest_agent/version.py', 'w') as git_file:
        git_file.write("\nclass Version(object):\n    VERSION = '" + VERSION + "'\n")
except:
    sys.stderr.write("You need to have installed 'git' to run the installer so it correctly determines its version")
    VERSION = "undetermined"

dev_extras = [
    'nose',
    'pep8',
    'tox'
]

docs_extras = [
    'Sphinx>=1.0',  # autodoc_member_order = 'bysource', autodoc_default_flags
    'sphinx_rtd_theme',
    'sphinxcontrib-programoutput'
]


setup(
    name='keychest_agent',
    version=VERSION,
    description='Keychest agent',
    url='https://gitlab.com/keychest/agent',
    author="Smart Arcs Ltd",
    author_email='support@keychest.net',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security'
    ],

    packages=find_packages(),
    namespace_packages=['keychest_agent'],
    package_data={'keychest_agent': ['LICENSE']},
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_extras,
        'docs': docs_extras,
    },

    entry_points={
        'console_scripts': [
            'keychest_agent = keychest_agent.main:main'
        ],
    }
)
