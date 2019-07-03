# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aisc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'aisc',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'MB',
    'author_email': 'mb@m1k.pw',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
