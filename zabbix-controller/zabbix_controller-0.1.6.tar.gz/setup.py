# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zabbix_controller']

package_data = \
{'': ['*']}

install_requires = \
['bullet>=2.1,<3.0', 'click>=7.0,<8.0', 'pyzabbix>=0.7.5,<0.8.0']

entry_points = \
{'console_scripts': ['zabbix_controller = '
                     'zabbix_controller.zabbix_controller:call_command']}

setup_kwargs = {
    'name': 'zabbix-controller',
    'version': '0.1.6',
    'description': '',
    'long_description': '# Zabbix CLI\n\n## Excecutable Command \n### `zabbix_controller --help`\n### `zabbix_controller hosts --help`\n### `zabbix_controller --apiserver-address http://loalhost:8081 hosts list`\n### `zabbix_controller -u username -p password hosts list`\n### `zabbix_controller -bu basicauth_username -bp basicauth_password hosts list`\n\n## Bad Command\n### `zabbix_controller hosts -u username -p password`',
    'author': 'hamadakafu',
    'author_email': 'kafu.h1998@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
