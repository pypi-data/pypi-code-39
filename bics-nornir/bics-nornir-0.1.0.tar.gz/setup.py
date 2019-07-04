# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bics_nornir',
 'bics_nornir.plugins',
 'bics_nornir.plugins.connections',
 'bics_nornir.plugins.tasks',
 'bics_nornir.plugins.tasks.data',
 'bics_nornir.plugins.tasks.networking',
 'bics_nornir.plugins.tasks.services']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2,<3',
 'ncclient>=0.6.3,<0.7.0',
 'nornir>=2.1,<3.0',
 'pydantic>=0.18.2,<0.19.0',
 'ruamel.yaml>=0.15.85,<0.16.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'bics-nornir',
    'version': '0.1.0',
    'description': 'Specific plugins for Nornir2',
    'long_description': "# Bics_nornir\nNornir is a Python automation framework that provides support for concurrent execution of tasks against a set of hosts. It comes with pluggable inventory and task capabilities to promote composability and reusability.\n\n`Bics_nornir` provides a set of BICS-developed plugins that addresses required functionality for communicating with the infrastructure as well as plugins as building blocks to implement _runbooks_. These plugins are:\n\n- `.../plugins/connections/ncclient`: a connection plugin that uses `ncclient` to communicate with devices using Netconf\n- `.../plugins/tasks/networking/nc`: a set of high-level task-plugins:\n    - `get_config`: retrieves (a part of) the device's configuration using netconf. The selection of a subtree of the configuration is through the `path` parameter\n    - `get`/ retrieves (a part of) the device's state information using netconf.\n    - `nc_configure`: sends a configuration (python object) to the device, with support of candidate/running comparision, dry-run and associated commit() and discard()\n- `.../plugins/tasks/data/load_intent`: loads intent files from a directory\n\n",
    'author': 'Walter De Smedt',
    'author_email': 'walter.de.smedt@gmail.com',
    'url': 'https://github.com/wdesmedt/bics_nornir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
