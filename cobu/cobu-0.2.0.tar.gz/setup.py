# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['cobu', 'cobu.commands']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.10,<3.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['cobu = cobu.cli:main']}

setup_kwargs = {
    'name': 'cobu',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'gilbus',
    'author_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
