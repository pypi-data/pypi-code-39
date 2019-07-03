# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aisc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'aisc',
    'version': '0.1.7',
    'description': 'AISC Helper Tools',
    'long_description': '![AISC](http://aisc.io/wp-content/uploads/2018/09/logo.svg)\n\n## AISC Tools\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aisc.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/a1sc/aisc_tools.svg)\n[![PyPI](https://img.shields.io/pypi/v/aisc.svg)](https://pypi.org/project/aisc/)\n\nSmall helper tools.\n\n## Installation\n\n`pip install aisc`\n\n## URL Tools\n\n```python3\nfrom aisc import url\n\n# Expand shortened url\nurl.expand(url)\n\n```\n',
    'author': 'MB',
    'author_email': 'mb@aisc.io',
    'url': 'https://github.com/a1sc/aisc_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
