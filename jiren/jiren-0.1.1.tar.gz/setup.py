# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jiren']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.10,<3.0']

entry_points = \
{'console_scripts': ['jiren = jiren.cli:main']}

setup_kwargs = {
    'name': 'jiren',
    'version': '0.1.1',
    'description': 'jinja2 template renderer',
    'long_description': '# jiren\n\njiren is an application that generates text from templates. The format of the template is based on jinja2.\n\n[![PyPI](https://img.shields.io/pypi/v/jiren.svg)](https://pypi.org/project/jiren/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren.svg)](https://pypi.org/project/jiren/)\n[![Build Status](https://travis-ci.com/speg03/jiren.svg?branch=master)](https://travis-ci.com/speg03/jiren)\n[![codecov](https://codecov.io/gh/speg03/jiren/branch/master/graph/badge.svg)](https://codecov.io/gh/speg03/jiren)\n\nRead this in Japanese: [日本語](https://github.com/speg03/jiren/blob/master/README.ja.md)\n\n## Installation\n\n```sh\npip install jiren\n```\n\n## Usage\n\nGenerate text from a template using the `jiren` command. The `jiren` command can read templates from stdin.\n\nCommand:\n```sh\necho "hello, {{ message }}" | jiren --message=world\n```\nOutput:\n```\nhello, world\n```\n\nIn this example, the template contains a variable called `message`. If you want to know more about template format, please refer to jinja2 document ( http://jinja.pocoo.org/ ).\n\nYou can use the help to check the variables defined in the template.\n\nCommand:\n```sh\necho "hello, {{ message }}" | jiren --help\n```\nOutput:\n```\nusage: jiren [-h] [--message MESSAGE]\n\noptional arguments:\n  -h, --help         show this help message and exit\n  --message MESSAGE\n```\n',
    'author': 'Takahiro Yano',
    'author_email': 'speg03@gmail.com',
    'url': 'https://github.com/speg03/jiren',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
