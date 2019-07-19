# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyartifactory', 'pyartifactory.models']

package_data = \
{'': ['*']}

install_requires = \
['email_validator>=1.0,<2.0', 'pydantic>=0.23.0,<0.24.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'pyartifactory',
    'version': '1.0.1',
    'description': 'Typed interactions with the Jfrog Artifactory REST API',
    'long_description': None,
    'author': 'Ananias CARVALHO',
    'author_email': 'carvalhoananias@hotmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
