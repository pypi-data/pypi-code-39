# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['advarchs']

package_data = \
{'': ['*']}

install_requires = \
['rarfile>=3.0,<4.0']

setup_kwargs = {
    'name': 'advarchs',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'elessarelfstone',
    'author_email': 'elessarelfstone@mail.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
