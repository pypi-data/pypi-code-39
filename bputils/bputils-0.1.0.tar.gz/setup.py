# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bputils']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.22,<2.0',
 'grpcio>=1.22,<2.0',
 'grpclib>=0.2.5,<0.3.0',
 'protobuf>=3.8,<4.0',
 'python-dotenv>=0.10.3,<0.11.0']

setup_kwargs = {
    'name': 'bputils',
    'version': '0.1.0',
    'description': 'BP utils',
    'long_description': None,
    'author': 'yokotoka',
    'author_email': 'hey@yokotoka.is',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
