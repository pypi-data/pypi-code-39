# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['google_jwt']

package_data = \
{'': ['*']}

install_requires = \
['python-jose>=3.0,<4.0']

setup_kwargs = {
    'name': 'google-jwt',
    'version': '0.1.0',
    'description': 'JWT Verification for Google issued JWT tokens, using Googles Well-Known OpenID Configurations and public keys.',
    'long_description': '# google-jwt\n',
    'author': 'William Vaughn',
    'author_email': 'vaughnwilld@gmail.com',
    'url': 'https://github.com/nackjicholson/google-jwt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
