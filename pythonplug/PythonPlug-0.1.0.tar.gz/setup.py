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
    'version': '0.1.0',
    'description': 'An ASGI web framework',
    'long_description': None,
    'author': 'Shen Li',
    'author_email': 'dustet@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
