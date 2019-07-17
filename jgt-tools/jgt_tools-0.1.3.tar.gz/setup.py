# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jgt_tools', 'jgt_tools.docs']

package_data = \
{'': ['*'], 'jgt_tools': ['data/*']}

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
    'version': '0.1.3',
    'description': 'A collection of tools for commmon package scripts',
    'long_description': 'JGT Tools\n=========\n\nJGT Tools is a collection of package helpers for common CLI functions within a properly-formatted repository.\n\n\nQuickstart\n----------\n\nJust include ``jgt_tools`` in your package VirtualEnv, and you\'ll have access to these CLI calls:\n\n- ``env-setup`` - set up the development environment with all packages and pre-commit checks\n- ``self-check`` - run self-checks/linters/etc. on your repository\n- ``run-tests`` - run your in-repo test suite\n- ``build-docs`` - build repo documentation locally\n- ``build-and-push-docs`` - both build the docs, then publish to your gh-pages branch\n\nDetails for each script can be found by calling with the ``--help`` flag.\n\nConfiguration\n-------------\n\nA number of the actions to be called can be customized\nin a ``[tool.jgt_tools]`` in your ``pyproject.toml`` file.\nAvailable values are:\n\n- ``env_setup_commands`` - a list of commands to be run under the ``env-setup`` call\n- ``self_check_commands`` - a list of commands to be run under the ``self-check`` call\n- ``run_tests_commands`` - a list of commands to be run under the ``run-tests`` call\n- ``doc_build_types`` - a list of types for doc construction:\n  - ``api`` is currently the only supported option\n\nFor example::\n\n    [tools.jgt_tools]\n    env_setup_commands = [\n        "poetry install",\n        "poetry run pip install other_package",\n        "./my_custom_setup_script.sh"\n    ]\n    doc_build_types = []\n\nwould run your specified commands for ``env-setup`` and skip the ``api`` doc builder.\n',
    'author': 'Brad Brown',
    'author_email': 'brad@bradsbrown.com',
    'url': 'https://jolly-good-toolbelt.github.io/jgt_tools/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
