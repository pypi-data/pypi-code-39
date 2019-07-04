# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['py_tps']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.14,<2.0']

setup_kwargs = {
    'name': 'py-tps',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ryanfeather',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
