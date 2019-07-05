# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['remotedata']
install_requires = \
['python-simpleconf', 'requests']

setup_kwargs = {
    'name': 'remotedata',
    'version': '0.0.1',
    'description': 'Accessing and caching remote data.',
    'long_description': '# remotedata\n\nAccessing and caching remote data for python.\n\n## Features\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'url': 'https://github.com/pwwang/remotedata',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
