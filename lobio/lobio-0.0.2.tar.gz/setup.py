# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lobio', 'lobio._version']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.73,<2.0']

entry_points = \
{'console_scripts': ['name = lobio:_version.get_name',
                     'upver = lobio:_version.pull_version',
                     'version = lobio:_version.get_version']}

setup_kwargs = {
    'name': 'lobio',
    'version': '0.0.2',
    'description': 'Extra utilities for BioPython',
    'long_description': '# LoBio\n\nKitchen sink utilities for BioPython\n\n## ImmutableSeqRecord\n\n',
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': 'https://www.github.com/jvrana/LoBio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
