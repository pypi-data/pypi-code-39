# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['narmock', 'narmock.templates']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.10,<3.0', 'pycparser>=2.19,<3.0']

entry_points = \
{'console_scripts': ['narmock = narmock.cli:main']}

setup_kwargs = {
    'name': 'narmock',
    'version': '0.1.1',
    'description': 'A minimal mocking utility for C projects.',
    'long_description': "# narmock\n\n[![Build Status](https://travis-ci.com/vberlier/narmock.svg?branch=master)](https://travis-ci.com/vberlier/narmock)\n[![PyPI](https://img.shields.io/pypi/v/narmock.svg)](https://pypi.org/project/narmock/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/narmock.svg)](https://pypi.org/project/narmock/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A minimal mocking utility for C projects.\n\n🚧 Work in progress 🚧\n\n## Contributing\n\nContributions are welcome. Feel free to open issues and suggest improvements. This project uses [poetry](https://poetry.eustace.io/) so you'll need to install it first if you want to be able to work with the project locally.\n\n```bash\n$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python\n```\n\nYou should now be able to install the required dependencies.\n\n```bash\n$ poetry install\n```\n\nThe code follows the [black](https://github.com/ambv/black) code style.\n\n```bash\n$ poetry run black narmock\n```\n\nYou can run the tests with `poetry run make -C tests`. The test suite is built with [Narwhal](https://github.com/vberlier/narwhal).\n\n```bash\n$ poetry run make -C tests\n```\n",
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'url': 'https://github.com/vberlier/narmock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
