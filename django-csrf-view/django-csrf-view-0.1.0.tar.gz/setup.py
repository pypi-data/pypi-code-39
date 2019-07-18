# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_csrf_view']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.0,<3.0']

setup_kwargs = {
    'name': 'django-csrf-view',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Дмитрий',
    'author_email': 'acrius@mail.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
