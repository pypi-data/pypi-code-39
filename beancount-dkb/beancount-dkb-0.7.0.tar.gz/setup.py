# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beancount_dkb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'beancount-dkb',
    'version': '0.7.0',
    'description': 'Beancount Importer for DKB CSV exports',
    'long_description': None,
    'author': 'Siddhant Goel',
    'author_email': 'me@sgoel.org',
    'url': 'https://github.com/siddhantgoel/beancount-dkb',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
