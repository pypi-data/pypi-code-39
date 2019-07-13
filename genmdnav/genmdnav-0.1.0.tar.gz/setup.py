# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['genmdnav']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['genmdnav = genmdnav:main']}

setup_kwargs = {
    'name': 'genmdnav',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
