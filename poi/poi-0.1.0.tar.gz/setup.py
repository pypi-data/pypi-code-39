# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['poi', 'poi.visitors']

package_data = \
{'': ['*']}

install_requires = \
['xlsxwriter>=1.1,<2.0']

setup_kwargs = {
    'name': 'poi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ryan Wang',
    'author_email': 'hwwangwang@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
