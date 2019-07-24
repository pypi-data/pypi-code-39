# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zabbix_controller', 'zabbix_controller.hosts']

package_data = \
{'': ['*']}

install_requires = \
['bullet>=2.1,<3.0', 'click>=7.0,<8.0', 'pyzabbix>=0.7.5,<0.8.0']

entry_points = \
{'console_scripts': ['zabbixctl = zabbix_controller.call_command:call_command']}

setup_kwargs = {
    'name': 'zabbix-controller',
    'version': '0.1.8',
    'description': '',
    'long_description': '# Zabbix CLI\nThis software is released under the MIT License, see LICENSE.txt.\n## Example\n### Valid Command\n`zabbix_controller -u username -p password hosts list`\n\n`zabbix_controller -u username -p password hosts -m name:^server$ list`\n### Invalid Command\n`zabbix_controller hosts -u username -p password list`\n\n`zabbix_controller -u username -p password hosts list -m name:^server$ `\n\n## zabbixctl [options] command ...\n### Options\nThese options are only set at `zabbixctl [options] command ...`.\n`zabbixctl command [options] ...` is not accepted.\n#### --help\n```bash\nzabbixctl --help\n```\n#### --apiserver-address, -aa\n```bash\nzabbixctl -aa http://localhost:8081\n```\n#### --username, -u, --password, -p\nUsed for zabbix login\n```bash\nzabbixctl --username Admin --password zabbix_password\n```\n#### --basicauth_username, -bu, --basicauth_password, -bp\nUsed for basic authentication\n```bash\nzabbixctl -bu alis -bp alis_password\n```\n#### --dry-run\nIf you set `--dry-run`, only get API is executed, then ZabbixCTL state is printed.\nCreate, update, delete like API is not executed.\n```bash\nzabbixctl --dry-run\n```\n\n## zabbixctl host `Options` `Command` ...\n### Options\n#### `-m, --match`\nSearch host using json like object.\nSearch key, then apply value.\nIn the example below, \nhosts which name key is including `some_name` is listed.\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' list\nzabbixctl hosts -m \'[{"name": "some_name"}]\' list\n```\nEach key, value pairs are chained by `and operator`.\nEach dicts are chained by `or operator`.\n\nThis command mean `("name": "some_name" and "hostid": "^1") or "name": "other_name"`.\n```bash\nzabbixctl hosts -m \'[{"name": "some_name", "hostid": "^1"}, {"name": "other_name"}]\' list\n```\n\n#### `-tr, --time-range`\nThis option is able to specify time range.\nIf you use --match at the same time, used by "and operator".\n```\nkey:[from]-[to]\n```\n`from` and `to` must be unixtime and can be omitted.\nThese commands are same and print host which disable property is included from 0 to now.\n```bash\nzabbixctl hosts -tr disable:0- list\nzabbixctl hosts -tr disable:- list\n```\nThis command mean `(("name": "some_name" and "hostid": "^1") or "name": "other_name") and (0 <= disable_until <= now)`.\n```bash\nzabbixctl hosts -m \'[{"name": "some_name", "hostid": "^1"}, {"name": "other_name"}]\' -tr \'disable_until:-\' list\n```\n\n\n### Commands\n#### `list`\nlist up host\n#### `delete`\ndelete host\n- options\n    - `-y, --yes`\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' delete -y\n```\n#### `disable`\ndisable host\n- options\n    - `-y, --yes`\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' disable -y\n```\n#### `update`\nupdate host\n- options\n    - `-d, --data`\n    - `-y, --yes`\n\nThese are same command.\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' update -d \'{"state": 1}\' -y\nzabbixctl hosts -m \'{"name": "some_name"}\' update -d \'{"state": "1"}\' -y\nzabbixctl hosts -m \'{"name": "some_name"}\' disable -y\n```\n\n## zabbixctl host graphs `Options` `Command`\n### Command\n#### `list`\n#### `delete`\n- options\n    - `-y, --yes`\n### Options\n#### `-m, --match`\n\nThis command delete graphs which is in hosts which is matched regex.\n```bash\nzabbixctl hosts -m \'{"name": "some_name"}\' graphs delete -y\n```\n\n## zabbixctl host interfaces `Options` `Command`\n### Command\n#### `list`\n#### `usedns`\nUse dns, not ipaddress\n- options\n    - `-y, --yes`\n\n#### `update`\nThese are same command.\n- options\n    - `-y, --yes`\n```bash\nzabbixctl hosts update -d \'{"useip": 0}\' -y\nzabbixctl hosts update -d \'{"useip": "0"}\' -y\nzabbixctl hosts usedns -y\n```\n',
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
