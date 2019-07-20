# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fetchy']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.32,<5.0']

entry_points = \
{'console_scripts': ['fetchy = fetchy:cli']}

setup_kwargs = {
    'name': 'fetchy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'thomas',
    'author_email': 'thomas.kluiters@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
