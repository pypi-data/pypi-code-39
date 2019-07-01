# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pyotr', 'pyotr.validation.requests', 'pyotr.validation.responses']

package_data = \
{'': ['*']}

install_requires = \
['http3>=0.6.3,<0.7.0',
 'openapi-core>=0.11.0,<0.12.0',
 'pytest-cov>=2.7,<3.0',
 'pyyaml>=5.1,<6.0',
 'requests>=2.22,<3.0',
 'starlette>=0.12.1,<0.13.0',
 'stringcase>=1.2,<2.0',
 'typing-extensions>=3.7,<4.0',
 'uvicorn>=0.8.2,<0.9.0']

setup_kwargs = {
    'name': 'pyotr',
    'version': '0.1.0',
    'description': 'OpenAPI-to-REST server and client frameworks for Python.',
    'long_description': None,
    'author': 'Berislav Lopac',
    'author_email': 'berislav@lopac.net',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
