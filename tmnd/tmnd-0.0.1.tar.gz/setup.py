# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tmnd', 'tmnd.elements']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'clint>=0.5.1,<0.6.0',
 'docker>=3.5.0,<4.0.0',
 'pastel>=0.1.0,<0.2.0',
 'python-slugify>=1.2,<2.0']

entry_points = \
{'console_scripts': ['tmnd = tmnd.tmnd:main']}

setup_kwargs = {
    'name': 'tmnd',
    'version': '0.0.1',
    'description': 'Quickstart your fullnode for DEX',
    'long_description': '# tmnd <a href="https://gitter.im/tomochain/tmnd"><img align="right" src="https://badges.gitter.im/gitterHQ/gitter.png"></a>\n\n| Branch  | Status | Coverage |\n| --- | --- | --- |\n| Master | [![Build Status](https://travis-ci.org/tomochain/tmnd.svg?branch=master)](https://travis-ci.org/tomochain/tmnd) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/tmnd/badge.svg?branch=master)](https://coveralls.io/github/tomochain/tmnd?branch=master) |\n| Develop | [![Build Status](https://travis-ci.org/tomochain/tmnd.svg?branch=develop)](https://travis-ci.org/tomochain/tmnd) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/tmnd/badge.svg?branch=develop)](https://coveralls.io/github/tomochain/tmnd?branch=develop) |\n\nTomo MasterNode (tmnd) is a cli tool to help you run a TomoChain masternode\n\n## Running and applying a masternode\n\nIf you are consulting this repo, it\'s probably because you want to run a masternode.\nFor complete guidelines on running a masternode candidate, please refer to the [documentation](https://docs.tomochain.com/masternode/requirements/).\n',
    'author': 'Hai Dam',
    'author_email': 'haidv@tomochain.com',
    'url': 'https://tomochain.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
