# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sphinx_gherkindoc']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=1.3',
 'behave>=1.2.6',
 'recommonmark>=0.4.0',
 'sphinx_rtd_theme>=0.3.1']

entry_points = \
{'console_scripts': ['sphinx-gherkinconfig = sphinx_gherkindoc.cli:config',
                     'sphinx-gherkindoc = sphinx_gherkindoc.cli:main']}

setup_kwargs = {
    'name': 'sphinx-gherkindoc',
    'version': '3.2.0',
    'description': 'A tool to convert Gherkin into Sphinx documentation',
    'long_description': None,
    'author': 'Lewis Franklin',
    'author_email': 'lewis.franklin@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
