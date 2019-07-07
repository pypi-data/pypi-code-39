# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['arg_dispatch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'arg-dispatch',
    'version': '0.1.2',
    'description': 'function can be dispatched by its arguments',
    'long_description': None,
    'author': 'zen-xu',
    'author_email': 'zen-xu@outlook.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
