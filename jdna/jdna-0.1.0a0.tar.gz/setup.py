# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jdna', 'jdna._version', 'jdna.regions']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.73,<2.0',
 'colorama>=0.4.1,<0.5.0',
 'networkx>=2.3,<3.0',
 'numpy>=1.16,<2.0',
 'primer3-py>=0.6.0,<0.7.0',
 'webcolors>=1.9,<2.0']

entry_points = \
{'console_scripts': ['name = jdna:_version.get_name',
                     'upver = jdna:_version.pull_version',
                     'version = jdna:_version.get_version']}

setup_kwargs = {
    'name': 'jdna',
    'version': '0.1.0a0',
    'description': '',
    'long_description': None,
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
