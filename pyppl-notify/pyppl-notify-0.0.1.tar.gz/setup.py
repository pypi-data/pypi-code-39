# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pyppl-notify']
install_requires = \
['panflute>=1.0.0,<2.0.0', 'pyppl>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'pyppl-notify',
    'version': '0.0.1',
    'description': 'Email notification for PyPPL',
    'long_description': '# pyppl-notify\nEmail notification for PyPPL\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'url': 'https://github.com/pwwang/pyppl-notify',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
