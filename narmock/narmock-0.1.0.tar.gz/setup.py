# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['narmock']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'narmock',
    'version': '0.1.0',
    'description': 'A minimal mocking utility for C projects.',
    'long_description': '# narmock\n\n[![PyPI](https://img.shields.io/pypi/v/narmock.svg)](https://pypi.org/project/narmock/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/narmock.svg)](https://pypi.org/project/narmock/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A minimal mocking utility for C projects.\n\n🚧 Work in progress 🚧\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'url': 'https://github.com/vberlier/narmock',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
