# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiopykube']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiopykube',
    'version': '0.1.0',
    'description': 'asyncio Pykube',
    'long_description': None,
    'author': 'Thibaut Le Page',
    'author_email': 'thilp@thilp.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
