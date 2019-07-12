# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ogc', 'ogc.api', 'ogc.commands', 'ogc.models']

package_data = \
{'': ['*']}

install_requires = \
['awscli>=1.16,<2.0',
 'boto3>=1.9,<2.0',
 'click>=7.0,<8.0',
 'jinja2>=2.10,<3.0',
 'juju-wait==2.7.0',
 'juju>=0.11.7,<0.12.0',
 'kv>=0.3.0,<0.4.0',
 'launchpadlib==1.10.6',
 'melddict>=1.0,<2.0',
 'python-box>=3.4,<4.0',
 'pyyaml-include>=1.1,<2.0',
 'pyyaml==3.13',
 'requests>=2.22,<3.0',
 'semver>=2.8,<3.0',
 'sh>=1.12,<2.0',
 'staticjinja>=0.3.5,<0.4.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['ogc = ogc:app.start']}

setup_kwargs = {
    'name': 'ogc',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Adam Stokes',
    'author_email': 'battlemidget@users.noreply.github.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
