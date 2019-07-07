# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['autopub']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'autopub',
    'version': '0.1.0a0',
    'description': '',
    'long_description': None,
    'author': 'Justin Mayer',
    'author_email': 'entrop@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
