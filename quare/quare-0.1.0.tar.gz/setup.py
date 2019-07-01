# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['quare']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0',
 'colorama>=0.4.1,<0.5.0',
 'dateparser>=0.7.1,<0.8.0',
 'keyring>=18.0,<19.0',
 'terminaltables>=3.1,<4.0',
 'websocket-client>=0.56.0,<0.57.0']

entry_points = \
{'console_scripts': ['quare = quare.cli:main']}

setup_kwargs = {
    'name': 'quare',
    'version': '0.1.0',
    'description': 'quare is a CLI client for Quip.',
    'long_description': None,
    'author': 'James Estevez',
    'author_email': 'j@jstvz.org',
    'url': 'https://github.com/jstvz/quare',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
