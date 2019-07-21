# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['caleb']

package_data = \
{'': ['*']}

install_requires = \
['crossref-commons>=0.0.5,<0.0.6']

setup_kwargs = {
    'name': 'caleb',
    'version': '0.3.0',
    'description': 'A tool to automatically retrieve bibtex entries',
    'long_description': None,
    'author': 'kevin lui',
    'author_email': 'kevinywlui@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
