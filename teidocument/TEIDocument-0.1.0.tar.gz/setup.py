# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['teidocument']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1,<2.0', 'lxml>=4.3,<5.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'teidocument',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'proprefenetre',
    'author_email': 'proprefenetre@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
