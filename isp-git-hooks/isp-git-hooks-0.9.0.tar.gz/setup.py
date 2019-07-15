# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['isp_git_hooks']

package_data = \
{'': ['*'], 'isp_git_hooks': ['pre_commit_hooks/*']}

install_requires = \
['pre-commit>=1.17,<2.0']

setup_kwargs = {
    'name': 'isp-git-hooks',
    'version': '0.9.0',
    'description': '',
    'long_description': None,
    'author': 'Marcel Hekking',
    'author_email': 'm.hekking@isprojects.nl',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
