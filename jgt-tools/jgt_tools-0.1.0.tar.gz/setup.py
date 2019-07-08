# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jgt_tools', 'jgt_tools.docs']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['build-and-push-docs = '
                     'jgt_tools.docs.build_docs:build_and_push',
                     'build-docs = jgt_tools.docs.build_docs:build',
                     'env-setup = jgt_tools.env_setup:main',
                     'run-tests = jgt_tools.run_tests:main',
                     'self-check = jgt_tools.self_check:main']}

setup_kwargs = {
    'name': 'jgt-tools',
    'version': '0.1.0',
    'description': 'A collection of tools for commmon package scripts',
    'long_description': None,
    'author': 'Brad Brown',
    'author_email': 'brad.brown@rackspace.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
