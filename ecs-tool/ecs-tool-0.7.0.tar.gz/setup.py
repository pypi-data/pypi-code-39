# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ecs_tool']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0',
 'click>=7.0,<8.0',
 'colorclass>=2.2,<3.0',
 'terminaltables>=3.1,<4.0']

entry_points = \
{'console_scripts': ['ecs = ecs_tool.cli:cli']}

setup_kwargs = {
    'name': 'ecs-tool',
    'version': '0.7.0',
    'description': 'CLI wrapper on top of "aws ecs" that tries to improve user experience',
    'long_description': '# ECS Tool\n[![Build Status](https://travis-ci.org/whisller/ecs-tool.svg?branch=master)](https://travis-ci.org/whisller/ecs-tool) [![PyPI](https://img.shields.io/pypi/v/ecs-tool.svg)](https://pypi.org/project/ecs-tool/) ![](https://img.shields.io/pypi/pyversions/ecs-tool.svg) ![](https://img.shields.io/pypi/l/ecs-tool.svg)\n\nCLI wrapper on top of "aws ecs" that tries to improve user experience and remove bottlenecks of work with AWS ECS.\n\nAWS is great platform, you can manage your ECS by web console or ecs-cli. \nBut both tools have their flaws, either speed or user interface.\n\nThat\'s why `ecs-tool` came to life, its aim is to be your day to day CLI tool for managing your ECS. \n\nIt is in early stage of development though.\n\n## Some screenshots\n[ecs services](https://github.com/whisller/ecs-tool/blob/master/screenshots/ecs-services-1.png) | [ecs tasks](https://github.com/whisller/ecs-tool/blob/master/screenshots/ecs-tasks-1.png) | [ecs task-definitions](https://github.com/whisller/ecs-tool/blob/master/screenshots/ecs-task-definitions-1.png)\n\n## Installation\n```sh\npip install ecs-tool\n```\n\n## What `ecs-tool` can do?\nList services, tasks and task definitions. All of those can be filtered by several attributes.\n\nYou can run task definition, here either it will automatically select latest version or you can specify number manually. \nThere is an option to wait for results of this execution.\n\n`ecs-tool` is grep friendly.\n',
    'author': 'Daniel Ancuta',
    'author_email': 'whisller@gmail.com',
    'url': 'https://github.com/whisller/ecs-tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
