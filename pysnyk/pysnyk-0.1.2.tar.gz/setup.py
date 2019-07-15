# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snyk']

package_data = \
{'': ['*']}

install_requires = \
['mashumaro>=1.7,<2.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'pysnyk',
    'version': '0.1.2',
    'description': 'A Python client for the Snyk API',
    'long_description': None,
    'author': 'Gareth Rushgrove',
    'author_email': 'garethr@snyk.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
