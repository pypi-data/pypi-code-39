# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kw', 'kw.platform', 'kw.platform.aiohttp', 'kw.platform.requests']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8,<3.0', 'webob>=1.8,<2.0', 'wrapt>=1.11,<2.0']

extras_require = \
{'aiohttp:python_version >= "3.5.3" and python_version < "4.0.0"': ['aiohttp>=3.5,<4.0'],
 'docs:python_version >= "3.5.3" and python_version < "4.0.0"': ['sphinx>=2.1,<3.0']}

setup_kwargs = {
    'name': 'kiwi-platform',
    'version': '0.2.1',
    'description': 'Company standards as code for Kiwi.com',
    'long_description': "# kiwi-platform-py\n\n[![CircleCI](https://circleci.com/gh/kiwicom/kiwi-platform-py.svg?style=svg)](https://circleci.com/gh/kiwicom/kiwi-platform-py)\n[![codecov](https://codecov.io/gh/kiwicom/kiwi-platform-py/branch/master/graph/badge.svg)](https://codecov.io/gh/kiwicom/kiwi-platform-py)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7594931404704cdc88d214f6b8898735)](https://www.codacy.com/app/bence/kiwi-platform-py?utm_source=github.com&utm_medium=referral&utm_content=kiwicom/kiwi-platform-py&utm_campaign=Badge_Grade)\n[![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/kiwicom/kiwi-platform-py.svg)](https://github.com/kiwicom/kiwi-platform-py/tags)\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kiwi-platform.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)\n\nCompany standards as code for Kiwi.com\n\n## Installation\n\nInstall with `pip install kiwi-platform`.\n\n## Contributing\n\n1. Check for open issues or open a fresh issue to start a discussion\n2. Fork [the repository](https://github.com/kiwicom/kiwi-platform-py) on GitHub.\n3. Send a pull request with your code!\n\nMerging will require a test which shows that the bug was fixed,\nor that the feature works as expected.\nFeel free to open a draft pull request though without such a test\nand ask for help with writing it if you're not sure how to.\n",
    'author': 'Bence Nagy',
    'author_email': 'bence@kiwi.com',
    'url': 'https://github.com/kiwicom/kiwi-platform-py/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
