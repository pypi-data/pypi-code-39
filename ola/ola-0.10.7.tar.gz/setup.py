# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ola', 'ola.rpc']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.1,<4.0']

setup_kwargs = {
    'name': 'ola',
    'version': '0.10.7',
    'description': 'Python bindings for OLA, available as a package',
    'long_description': None,
    'author': 'Justin Cummins',
    'author_email': 'justin@samosec.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
