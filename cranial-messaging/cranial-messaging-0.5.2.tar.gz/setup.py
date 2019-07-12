# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cranial',
 'cranial.connectors',
 'cranial.datastore',
 'cranial.datastore.adapters',
 'cranial.keyvalue',
 'cranial.listeners',
 'cranial.messaging',
 'cranial.messaging.adapters']

package_data = \
{'': ['*'],
 'cranial': ['common/*', 'servicediscovery/*'],
 'cranial.messaging': ['test/*']}

install_requires = \
['boto3>=1.9,<2.0',
 'cachetools>=3.1.1,<4.0.0',
 'docopt>=0.6.2,<0.7.0',
 'psycopg2-binary>=2.6.2,<3.0.0',
 'pyyaml>=5.1,<6.0',
 'recordclass>=0.11.1,<0.12.0',
 'requests-futures>=1.0.0,<2.0.0',
 'requests>=2.21,<3.0',
 'smart_open>=1.8.3,<2.0.0',
 'ujson>=1.3.5,<2.0.0',
 'zmq>=0.0.0,<0.0.1']

entry_points = \
{'console_scripts': ['cranial = cranial.scripts:cranial']}

setup_kwargs = {
    'name': 'cranial-messaging',
    'version': '0.5.2',
    'description': 'Abstractions for high-level communication between data stores, message brokers, and micro-services.',
    'long_description': None,
    'author': 'Matt Chapman et al.',
    'author_email': 'Matt@NinjitsuWeb.com',
    'url': 'https://github.com/tribune/cranial-messaging',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
