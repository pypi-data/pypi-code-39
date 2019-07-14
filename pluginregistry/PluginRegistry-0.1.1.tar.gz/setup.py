import pathlib
import setuptools
import distutils
import subprocess
import re

install_requires = [
    "setuptools",
]

test_requires = [
    "coveralls",
    "pytest",
    "pytest-clarity",
    "pytest-cov",
    "pytest-mock",
    "pytest-sugar",
]

# NOTE:  This works only because there are no external dependencies.
from pregistry import __version__

setuptools.setup(
    name                          = "PluginRegistry",
    packages                      = setuptools.find_packages(),
    version                       = __version__,
    license                       = 'MIT License',
    description                   = 'Plugin Registry for Python',
    long_description_content_type = "text/markdown",
    author                        = 'David Morris',
    author_email                  = 'selcouth.dev@gmail.com',
    url                           = 'https://gitlab.com/othalan/plugin-registry',
    include_package_data          = True,
    zip_safe                      = True,
    install_requires              = install_requires,
    extras_require                = {
        "test": test_requires,
    },
    long_description              = """
A python plugin manager which provides:

* A tree based structure for plugin registry and organization
* Automatic plugin discovery via setuptools entry points
* import plugins using the registry path as namespace modules
""",
    classifiers = [
        # complete classifier list: https://pypi.org/classifiers/
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
)

