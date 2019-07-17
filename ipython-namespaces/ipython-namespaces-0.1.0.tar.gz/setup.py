# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ipython_namespaces']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=5.0,<6.0']

setup_kwargs = {
    'name': 'ipython-namespaces',
    'version': '0.1.0',
    'description': 'Extension for IPython/Jupyter Notebooks that adds namespaces that you can enter and re-enter',
    'long_description': None,
    'author': 'Denis Drescher',
    'author_email': 'denis.drescher@claviger.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
