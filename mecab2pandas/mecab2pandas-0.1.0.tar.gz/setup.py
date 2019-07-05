# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mecab2pandas', 'mecab2pandas.exception']

package_data = \
{'': ['*']}

install_requires = \
['mecab-python3>=0.996.2,<0.997.0', 'pandas>=0.24.2,<0.25.0']

setup_kwargs = {
    'name': 'mecab2pandas',
    'version': '0.1.0',
    'description': 'MeCab to pandas',
    'long_description': None,
    'author': 'Lucky',
    'author_email': 'phatbowie@gmail.com',
    'url': 'https://github.com/Lucky-Mano/mecab2pandas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
