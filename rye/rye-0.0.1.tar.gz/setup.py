# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['rye']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'colorama>=0.4,<0.5',
 'settingscascade>=0.3.4,<0.4.0',
 'toml>=0.10,<0.11',
 'virtualenv>=16.6,<17.0']

entry_points = \
{'console_scripts': ['rye = rye.__main__:cli']}

setup_kwargs = {
    'name': 'rye',
    'version': '0.0.1',
    'description': '',
    'long_description': '#!/usr/bin/env bash',
    'author': 'Paul Becotte',
    'author_email': 'pjbecotte@gmail.com',
    'url': 'https://gitlab.com/pjbecotte/rye',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
