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
    'version': '0.0.2',
    'description': 'CLI wrapper on top of "aws ecs" that tries to improve user experience',
    'long_description': '# ECS Tools\n',
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
