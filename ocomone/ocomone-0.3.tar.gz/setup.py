# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ocomone']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ocomone',
    'version': '0.3',
    'description': 'Common helper library by Anton Kachurin',
    'long_description': None,
    'author': 'Anton Kachurin',
    'author_email': 'katchuring@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
