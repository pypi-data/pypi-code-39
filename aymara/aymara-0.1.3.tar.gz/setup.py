# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aymara']

package_data = \
{'': ['*']}

install_requires = \
['PySide2>=5.12,<6.0',
 'docker>=4.0.2,<5.0.0',
 'pyconll>=2.0,<3.0',
 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'aymara',
    'version': '0.1.3',
    'description': 'Python bindings to the LIMA linguistic analyzer',
    'long_description': None,
    'author': 'Gael de Chalendar',
    'author_email': 'gael.de-chalendar@cea.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
