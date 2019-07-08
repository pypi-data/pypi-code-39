import sys
from setuptools import setup

from utilitiespackage.settings import *

assert sys.version_info >= MINIMUM_PYTHON_VERSION

setup(
    name="utilities-package",
    version=VERSION,
    description="utilities package",
    url="https://github.com/terminal-labs/utilities-package",
    author="Terminal Labs",
    author_email="solutions@terminallabs.com",
    license="see LICENSE file",
    packages=["utilitiespackage", "utilitiespackage.standard", "utilitiespackage.tests"],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "scipy",
        "setuptools",
        "six",
        "bash",
        "configparser",
        "unidecode",
        "uritools",
        "simplejson",
        "tailer",
        "pytz",
        "termcolor",
        "texttable",
        "schedule",
        "python-dateutil",
        "beautifulsoup4",
        "cssutils",
        "base58",
        "bcrypt",
        "aiohttp",
        "requests",
        "tornado",
        "cherrypy",
        "bottle",
        "flask",
        "click",
        "Jinja2",
        "coverage",
        "pycontracts",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "pytest-click",
        "pytest-pylint",
        "black",
        "flake8",
        "radon",
        "cli-passthrough",
    ],
    entry_points="""
        [console_scripts]
        utilitiespackage=utilitiespackage.__main__:main
    """,
)
