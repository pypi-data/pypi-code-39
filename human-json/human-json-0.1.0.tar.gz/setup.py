# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['human_json']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'human-json',
    'version': '0.1.0',
    'description': 'Transform JSON Objects to human readable strings',
    'long_description': None,
    'author': 'Kuba Clark',
    'author_email': 'jakub.clark@protonmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
