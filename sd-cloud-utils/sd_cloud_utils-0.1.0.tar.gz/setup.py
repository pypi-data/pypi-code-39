# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sd_cloud_utils', 'sd_cloud_utils.aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0']

setup_kwargs = {
    'name': 'sd-cloud-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sean Davis',
    'author_email': 'seandavi@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
