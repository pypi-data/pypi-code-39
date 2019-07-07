# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keat_scripts', 'keats']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.1.3,<0.2.0', 'termcolor>=1.1,<2.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['keats = keats:main']}

setup_kwargs = {
    'name': 'keats',
    'version': '0.2.17',
    'description': '',
    'long_description': None,
    'author': 'jvrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
