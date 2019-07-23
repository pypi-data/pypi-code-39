# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['laserembeddings']

package_data = \
{'': ['*'], 'laserembeddings': ['data/.gitkeep']}

install_requires = \
['numpy>=1.15.4,<2.0.0',
 'sacremoses>=0.0.21,<0.0.22',
 'subword-nmt>=0.3.6,<0.4.0',
 'torch>=1.0.1.post2,<2.0.0']

setup_kwargs = {
    'name': 'laserembeddings',
    'version': '0.1.0',
    'description': 'Production-ready LASER multilingual embeddings',
    'long_description': None,
    'author': 'yannvgn',
    'author_email': 'hi@yannvgn.io',
    'url': 'https://github.com/yannvgn/laserembeddings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
