# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

modules = \
['__init__']
setup_kwargs = {
    'name': 'hexlet-pairs',
    'version': '0.1.2',
    'description': "A SICP'ish functional pairs implemented in Python",
    'long_description': "### hexlet-pairs\n\nA SICP'ish Functional Pairs implemented in Python.\n\n### Usage\n\n<!-- This code will be doctested. Do not touch the markup! -->\n\n    >>> from hexlet import pairs\n    >>> p = pairs.cons(42, 'foo')\n    >>> pairs.is_pair(p)\n    True\n    >>> pairs.car(p)\n    42\n    >>> pairs.cdr(p)\n    'foo'\n    >>> print(pairs.to_string(p))\n    (42, 'foo')\n",
    'author': 'Hexlet Team',
    'author_email': 'info@hexlet.io',
    'url': 'https://github.com/hexlet-components/python-pairs',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
