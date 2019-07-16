# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fds', 'fds.auth', 'fds.auth.signature', 'fds.model']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete>=1.9,<2.0', 'click>=7.0,<8.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'galaxy-fds-sdk',
    'version': '1.4.23',
    'description': 'Python sdk for Galaxy FDS',
    'long_description': None,
    'author': 'hujianxin',
    'author_email': 'hujianxin@xiaomi.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
