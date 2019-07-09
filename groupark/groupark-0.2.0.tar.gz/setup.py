# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['groupark']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'groupark',
    'version': '0.2.0',
    'description': 'Quick Python Aggregations',
    'long_description': None,
    'author': 'eecheverry',
    'author_email': 'eecheverry@nubark.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
