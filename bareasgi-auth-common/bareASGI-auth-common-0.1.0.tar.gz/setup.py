# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bareasgi_auth_common']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.7,<2.0', 'bareclient>=2.0,<3.0']

setup_kwargs = {
    'name': 'bareasgi-auth-common',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rob Blackbourn',
    'author_email': 'rblackbourn@ugsb-rbla01.bhdgsystematic.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
