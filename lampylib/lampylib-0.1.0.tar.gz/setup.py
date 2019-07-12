# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lampylib']

package_data = \
{'': ['*']}

install_requires = \
['python-rtmidi']

entry_points = \
{'console_scripts': ['lampy = lampylib.__main__:main']}

setup_kwargs = {
    'name': 'lampylib',
    'version': '0.1.0',
    'description': 'Launchpad Mini python library',
    'long_description': "|Build Status| |Coverage|\n\n=============================================================\nLampy: **La**\\ unchpad **M**\\ ini **p**\\ ython librar\\ **y**\n=============================================================\n\n.. image:: https://github.com/pkulev/lampy/raw/master/launchpad.jpg\n\nRequirements\n============\n\n* Python >= 3.7\n* python-rtmidi\n* TODO\n* TODO\n\nInstallation\n============\n\nFor usage only\n--------------\n\nUnfortunately name **lampy** was already in use in PyPI.\n\n.. code-block:: console\n\n   # via pipsi\n   $ pipsi install lampylib\n\n   # via pip\n   $ pip install --user lampylib\n\nFor development\n---------------\n\nYou need `poetry <https://poetry.eustace.io/>`__ installed.\n(It's great tool! Check it out, please.)\n\n.. code-block:: console\n\n   $ poetry install --develop .\n\nTesting\n=======\n\n* TODO\n\nDocumentation\n=============\n\n* TODO\n\n.. |Build Status| image:: https://travis-ci.org/pkulev/lampy.svg?branch=master\n   :target: https://travis-ci.org/pkulev/lampy\n.. |Coverage| image:: https://codecov.io/gh/pkulev/lampy/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/pkulev/lampy\n",
    'author': 'Pavel Kulyov',
    'author_email': 'kulyov.pavel@gmail.com',
    'url': 'https://github.com/pkulev/lampy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
