# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

modules = \
['__init__']
install_requires = \
['hexlet-pairs>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'hexlet-points',
    'version': '0.1.0',
    'description': "A SICP'ish Points implemented in Python using hexlet-pairs",
    'long_description': "### hexlet-points\n\nA SICP'ish Points implemented in Python using hexlet-pairs.\n\n### Usage\n\n<!-- This code will be doctested. Do not touch the markup! -->\n\n    >>> from hexlet import points\n    >>> p = points.make(100, 200)\n    >>> print(points.to_string(p))\n    (100, 200)\n    >>> points.get_quadrant(p)\n    1\n    >>> points.get_x(p)\n    100\n    >>> points.get_y(p)\n    200\n",
    'author': 'Hexlet Team',
    'author_email': 'info@hexlet.io',
    'url': 'https://github.com/hexlet-components/python-points',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
