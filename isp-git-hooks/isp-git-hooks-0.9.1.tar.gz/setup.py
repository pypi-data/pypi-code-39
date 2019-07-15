# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['isp_git_hooks']

package_data = \
{'': ['*'], 'isp_git_hooks': ['pre_commit_hooks/*']}

install_requires = \
['pre-commit>=1.17,<2.0']

entry_points = \
{'console_scripts': ['check-deze = '
                     'isp_git_hooks.pre_commit_hooks.check_deze:main']}

setup_kwargs = {
    'name': 'isp-git-hooks',
    'version': '0.9.1',
    'description': '',
    'long_description': None,
    'author': 'Marcel Hekking',
    'author_email': 'm.hekking@isprojects.nl',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
