# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aleister', 'aleister.question']

package_data = \
{'': ['*']}

install_requires = \
['prompt_toolkit>=2.0,<3.0']

setup_kwargs = {
    'name': 'aleister',
    'version': '0.1.1',
    'description': 'library for CUI wizard',
    'long_description': None,
    'author': 'Hirotomo Moriwaki',
    'author_email': 'philopon.dependence@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
