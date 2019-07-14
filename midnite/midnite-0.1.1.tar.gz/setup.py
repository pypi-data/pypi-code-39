# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['midnite',
 'midnite.uncertainty',
 'midnite.visualization',
 'midnite.visualization.base',
 'midnite.visualization.base.methods']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0',
 'opencv-python>=4.0,<5.0',
 'pillow>=6.1,<7.0',
 'torch==1.1',
 'tqdm>=4.31,<5.0']

setup_kwargs = {
    'name': 'midnite',
    'version': '0.1.1',
    'description': 'This is a framework for visualization and uncertainty in CNNs.',
    'long_description': None,
    'author': 'Christina Aigner, Fabian Huch',
    'author_email': None,
    'url': 'https://luminovo.gitlab.io/midnite',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
