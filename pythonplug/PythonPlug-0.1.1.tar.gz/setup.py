# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['PythonPlug', 'PythonPlug.contrib', 'PythonPlug.utils']

package_data = \
{'': ['*'], 'PythonPlug.contrib': ['parser/*', 'plug/*']}

install_requires = \
['Werkzeug>=0.15.4,<0.16.0', 'multidict>=4.5,<5.0']

setup_kwargs = {
    'name': 'pythonplug',
    'version': '0.1.1',
    'description': 'An ASGI web framework',
    'long_description': "# PythonPlug\n\n[![CircleCI](https://circleci.com/gh/ericls/PythonPlug.svg?style=shield)](https://circleci.com/gh/ericls/PythonPlug)\n[![Code Coverage](https://codecov.io/gh/ericls/PythonPlug/branch/master/graph/badge.svg)](https://codecov.io/gh/ericls/PythonPlug)\n[![Python Version](https://img.shields.io/pypi/pyversions/PythonPlug.svg)](https://pypi.org/project/PythonPlug/)\n[![PyPI Package](https://img.shields.io/pypi/v/PythonPlug.svg)](https://pypi.org/project/PythonPlug/)\n[![License](https://img.shields.io/pypi/l/PythonPlug.svg)](https://github.com/ericls/PythonPlug/blob/master/LICENSE.md)\n\n\nASGI web framework inspired by Elixir's [Plug](https://github.com/elixir-plug/plug)\n",
    'author': 'Shen Li',
    'author_email': 'dustet@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
