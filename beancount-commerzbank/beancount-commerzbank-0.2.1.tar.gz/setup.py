# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beancount_commerzbank']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'beancount-commerzbank',
    'version': '0.2.1',
    'description': 'Beancount Importer for Commerzbank (DE) CSV exports',
    'long_description': None,
    'author': 'Siddhant Goel',
    'author_email': 'me@sgoel.org',
    'url': 'https://github.com/siddhantgoel/beancount-commerzbank',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
