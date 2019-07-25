# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simplecalc', 'simplecalc.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'toml>=0.10.0,<0.11.0']

extras_require = \
{'doc': ['sphinx>=2.1,<3.0', 'sphinx_rtd_theme>=0.4.3,<0.5.0']}

entry_points = \
{'console_scripts': ['simplecalc = simplecalc.cli:simplecalc']}

setup_kwargs = {
    'name': 'simplecalc',
    'version': '0.1.0',
    'description': 'A simple calculator to demonstrate python tooling',
    'long_description': 'calculator.py\n=============\n\n|BuildStatus| |DocStatus| |Coverage| |CodeStyle| |License|\n\n`simplecalc` is an example project to show how to set up an open source project from scratch.\n\n.. |BuildStatus| image:: https://dev.azure.com/adithyabsk/simplecalc/_apis/build/status/adithyabsk.simplecalc?branchName=master\n   :target: https://dev.azure.com/adithyabsk/simplecalc/_build/latest?definitionId=1&branchName=master\n\n.. |DocStatus| image:: https://readthedocs.org/projects/simplecalc/badge/?version=latest\n  :target: https://simplecalc.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\n.. |Coverage| image:: https://img.shields.io/azure-devops/coverage/adithyabsk/simplecalc/1.svg\n  :target: https://dev.azure.com/adithyabsk/simplecalc/_build/latest?definitionId=1&branchName=master\n  :alt: Coverage\n\n.. |CodeStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :target: https://github.com/ambv/black\n  :alt: Code Style\n\n.. |License| image:: https://img.shields.io/github/license/adithyabsk/simplecalc.svg\n  :target: https://github.com/adithyabsk/simplecalc/blob/master/LICENSE\n  :alt: License\n\nRead the Blog Post\n------------------\nThe blog talks about how this project was set up {LINK ME}.\n\nDocumentation\n-------------\n`Read the docs!`_\n\n.. _Read the docs!: https://simplecalc.readthedocs.io/en/latest/index.html\n',
    'author': 'Adithya Balaji',
    'author_email': 'adithyabsk@gmail.com',
    'url': 'https://simplecalc.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
