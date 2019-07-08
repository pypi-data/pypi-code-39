# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aeidon',
 'aeidon.agents',
 'aeidon.agents.test',
 'aeidon.files',
 'aeidon.files.test',
 'aeidon.markups',
 'aeidon.markups.test',
 'aeidon.test']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0,<4.0', 'pyenchant>=2.0,<3.0']

setup_kwargs = {
    'name': 'aeidon',
    'version': '1.6.0',
    'description': 'aeidon is a Python package for reading, writing and manipulating text-based subtitle files. It is used by the gaupol package, which provides a subtitle editor with a GTK+ user interface.',
    'long_description': None,
    'author': 'Jack Laxson',
    'author_email': 'jackjrabbit+pypi@gmail.com',
    'url': 'https://otsaloma.io/gaupol/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
