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
    'version': '0.1.6',
    'description': 'A minimal mocking utility for C projects.',
    'long_description': '# 🎣 narmock\n\n[![Build Status](https://travis-ci.com/vberlier/narmock.svg?branch=master)](https://travis-ci.com/vberlier/narmock)\n[![PyPI](https://img.shields.io/pypi/v/narmock.svg)](https://pypi.org/project/narmock/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/narmock.svg)](https://pypi.org/project/narmock/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A minimal mocking utility for C projects.\n\n**🚧 Work in progress 🚧**\n\nNarmock identifies the mocks being used in your tests and generates easy-to-use implementations with a slick API.\n\n```c\n#include <time.h>\n\n#include "__mocks__.h"\n#include "narwhal.h"\n\nTEST(example)\n{\n    MOCK(time)->mock_return(42);\n    ASSERT_EQ(time(NULL), 42);\n}\n```\n\n> Most of the examples in this README are tests written with [Narwhal](https://github.com/vberlier/narwhal) but Narmock can be used with other test frameworks and anywhere in regular source code.\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install narmock\n```\n\n## Getting started\n\nThe command-line utility provides three essential commands that should make it possible to integrate Narmock in any kind of build system.\n\n```\n$ narmock --help\nusage: narmock [-h] (-g <file> | -d <file> | -f) [-p <string>] [<file>]\n\nA minimal mocking utility for C projects.\n\npositional arguments:\n  <file>       expanded code or generated mocks\n\noptional arguments:\n  -h, --help   show this help message and exit\n  -g <file>    generate mocks\n  -d <file>    extract declarations\n  -f           output linker flags\n  -p <string>  getter prefix\n```\n\n_TODO_\n\n## Contributing\n\nContributions are welcome. Feel free to open issues and suggest improvements. This project uses [poetry](https://poetry.eustace.io/) so you\'ll need to install it first if you want to be able to work with the project locally.\n\n```bash\n$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python\n```\n\nYou should now be able to install the required dependencies.\n\n```bash\n$ poetry install\n```\n\nThe code follows the [black](https://github.com/ambv/black) code style.\n\n```bash\n$ poetry run black narmock\n```\n\nYou can run the tests with `poetry run make -C tests`. The test suite is built with [Narwhal](https://github.com/vberlier/narwhal).\n\n```bash\n$ poetry run make -C tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/narmock/blob/master/LICENSE)\n',
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
