# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lobio']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.73,<2.0']

setup_kwargs = {
    'name': 'lobio',
    'version': '0.0.15',
    'description': 'Extra utilities for BioPython',
    'long_description': '# LoBio\n\nKitchen sink utilities for BioPython\n\n## ImmutableSeqRecord\n\n',
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': 'https://www.github.com/jvrana/LoBio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
