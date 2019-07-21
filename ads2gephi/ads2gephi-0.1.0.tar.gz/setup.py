# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ads2gephi']

package_data = \
{'': ['*']}

install_requires = \
['ads>=0.12.3,<0.13.0',
 'click>=7.0,<8.0',
 'configparser>=3.7,<4.0',
 'hypothesis>=4.28,<5.0',
 'igraph>=0.1.11,<0.2.0',
 'pytest>=5.0,<6.0',
 'sqlalchemy>=1.3,<2.0']

entry_points = \
{'console_scripts': ['ads2gephi = ads2gephi.cli:main']}

setup_kwargs = {
    'name': 'ads2gephi',
    'version': '0.1.0',
    'description': 'A command line tool for querying and modeling citation networks from the Astrophysical Data System (ADS) in a format compatible with Gephi',
    'long_description': None,
    'author': 'Theo Costea',
    'author_email': 'theo.costea@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
