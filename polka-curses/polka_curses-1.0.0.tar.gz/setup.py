# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['polka_curses', 'polka_curses.views', 'polka_curses.views.widgets']

package_data = \
{'': ['*']}

install_requires = \
['polka>=2.4,<3.0', 'urwid>=2.0,<3.0']

entry_points = \
{'console_scripts': ['polka = polka_curses.main:main']}

setup_kwargs = {
    'name': 'polka-curses',
    'version': '1.0.0',
    'description': 'The curses interface for the Polka website (https://polka.academy/)',
    'long_description': '[![Build Status](https://travis-ci.org/dmkskn/polka_curses.svg?branch=master)](https://travis-ci.org/dmkskn/polka_curses)',
    'author': 'Dima Koskin',
    'author_email': 'dmksknn@gmail.com',
    'url': 'https://github.com/dmkskn/polka_curses/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
