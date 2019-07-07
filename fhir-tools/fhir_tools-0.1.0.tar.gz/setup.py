# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fhir_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fhir-tools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': "Pavel 'Blane' Tuchin",
    'author_email': 'blane.public@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
