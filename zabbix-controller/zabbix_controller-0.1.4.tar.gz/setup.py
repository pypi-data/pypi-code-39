# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zabbix_controller']

package_data = \
{'': ['*']}

install_requires = \
['bullet', 'click>=7.0,<8.0', 'pyzabbix']

entry_points = \
{'console_scripts': ['main = zabbix_controller:main']}

setup_kwargs = {
    'name': 'zabbix-controller',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'hamadakafu',
    'author_email': 'kafu.h1998@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
