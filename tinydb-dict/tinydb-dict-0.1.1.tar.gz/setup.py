# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tinydb_dict']

package_data = \
{'': ['*']}

install_requires = \
['tinydb>=3.13,<4.0']

setup_kwargs = {
    'name': 'tinydb-dict',
    'version': '0.1.1',
    'description': 'Simple dict-like class for TinyDB',
    'long_description': "# tinydb-config\nSimple dict-like class for TinyDB\n\n## Usage\n```python\nfrom tinydb import TinyDB\nfrom tinydb.storages import MemoryStorage\nfrom tinydb_dict import TinyDBDict\n\n# Pass any TinyDB argument to TinyDBDict\nconfig = TinyDBDict('db.json')\nconfig = TinyDBDict(storage=MemoryStorage)\n\n# Then use it as a dictionary\nconfig['key'] = 1\nconfig['key']  # 1\nconfig['key'] = 2\nconfig['key']  # 2\nconfig['unknown_key']  # KeyError: 'unknown_key'\n\n# You can also pass a TinyDB instance\ndb = TinyDB('db.json')\nconfig = TinyDBDict(tinydb=db)\n```\n",
    'author': 'Ali Ghahraei',
    'author_email': 'aligf94@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
