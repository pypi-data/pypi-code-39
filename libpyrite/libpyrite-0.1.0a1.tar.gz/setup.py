# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['libpyrite',
 'libpyrite.harness',
 'libpyrite.nn',
 'libpyrite.nn.modules',
 'libpyrite.optim',
 'libpyrite.utils',
 'libpyrite.utils.data']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.3,<2.0',
 'torch>=1.1,<2.0',
 'torchvision>=0.3.0,<0.4.0',
 'tqdm>=4.32,<5.0']

setup_kwargs = {
    'name': 'libpyrite',
    'version': '0.1.0a1',
    'description': 'PyTorch utility library',
    'long_description': None,
    'author': 'Miller Wilt',
    'author_email': 'miller@pyriteai.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
