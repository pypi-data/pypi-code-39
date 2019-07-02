# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ogc', 'ogc.api', 'ogc.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'jinja2>=2.10,<3.0',
 'juju-wait==2.7.0',
 'juju>=0.11.7,<0.12.0',
 'kv>=0.3.0,<0.4.0',
 'launchpadlib==1.10.6',
 'melddict>=1.0,<2.0',
 'pyyaml==3.13',
 'semver>=2.8,<3.0',
 'sh>=1.12,<2.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['ogc = ogc:app.start']}

setup_kwargs = {
    'name': 'ogc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Adam Stokes',
    'author_email': 'battlemidget@users.noreply.github.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
