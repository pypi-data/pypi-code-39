# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fds', 'fds.auth', 'fds.auth.signature', 'fds.model']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete>=1.9,<2.0', 'click>=7.0,<8.0', 'requests>=2.21,<3.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['pathlib2>=2.2,<3.0',
                                                         'future>=0.17.1,<0.18.0']}

entry_points = \
{'console_scripts': ['fds = fds.fds_cli:main', 'fdscli = fds.fdscli_cli:main']}

setup_kwargs = {
    'name': 'galaxy-fds-sdk-beta',
    'version': '1.4.24',
    'description': 'Python sdk for Galaxy FDS',
    'long_description': None,
    'author': 'hujianxin',
    'author_email': 'hujianxin@xiaomi.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
