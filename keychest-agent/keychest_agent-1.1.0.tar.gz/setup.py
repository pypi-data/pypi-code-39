import datetime
import os
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
    print("Python 2 and Python 3.5 or lower are not supported")
    exit(-1)

# crate a git_version file
git_version_b = subprocess.check_output(['git', 'describe', '--always'], stderr=subprocess.DEVNULL)  # returns bytes
VERSION = git_version_b.decode().strip()
resource_package = __name__
resource_path = 'data/git_version'
data_dir = pkg_resources.resource_filename(resource_package, 'data')
data_filename = pkg_resources.resource_filename(resource_package, resource_path)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

with open(data_filename, 'w') as git_file:
    git_file.write(VERSION)


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
    long_description=open('README.md').read(),
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
    package_data={'keychest_agent': ['data/*', 'LICENSE']},
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
