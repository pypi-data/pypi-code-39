# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ezpg']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.8,<3.0']

setup_kwargs = {
    'name': 'ezpg',
    'version': '0.1.1b0',
    'description': '',
    'long_description': None,
    'author': 'Matt Chapman',
    'author_email': 'Matt@NinjitsuWeb.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
