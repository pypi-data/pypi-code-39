# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['katcr', 'katcr.engines']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.7.4,<0.8.0',
 'cutie>=0.2.2,<0.3.0',
 'pygogo>=0.12.0,<0.13.0',
 'requests>=2.22,<3.0',
 'robobrowser>=0.5.3,<0.6.0',
 'telepot>=12.7,<13.0',
 'torrentmirror>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['katcr = katcr:main']}

setup_kwargs = {
    'name': 'katcr',
    'version': '2.0.0',
    'description': 'KickassTorrents CLI and Telegram bot',
    'long_description': None,
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
