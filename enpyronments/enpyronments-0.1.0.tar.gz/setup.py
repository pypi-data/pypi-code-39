# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['enpyronments']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enpyronments',
    'version': '0.1.0',
    'description': 'A settings loading library inspired by Django and Node.js',
    'long_description': None,
    'author': 'Stephen Lowery',
    'author_email': 'slowery@markelcorp.com',
    'url': 'https://github.com/stephen1000/enpyronments',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
