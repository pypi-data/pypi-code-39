# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['py_tps']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.14,<2.0']

setup_kwargs = {
    'name': 'py-tps',
    'version': '0.1.1',
    'description': 'This is a simple library for reading and writing .tps files as created and used by the tpsDig landmarking tool created by F. James Rohlf.  https://life.bio.sunysb.edu/morph/',
    'long_description': 'This is a simple library for reading and writing .tps files as created and used by the tpsDig landmarking tool\ncreated by F. James Rohlf.  https://life.bio.sunysb.edu/morph/\n\nInstallation\n============\nInstallation is managed via poetry. https://pypi.org/project/poetry/\n\nTo install, first install poetry.\n*Note for conda users*\nIn order to use a conda environment with poetry, you must first configure poetry to use your conda environment and\nnot create a new virtualenv environment. Example::\n\n    poetry config settings.virtualenvs.path $CONDA_ENV_PATH\n    poetry config settings.virtualenvs.create 0\n\nThen run::\n\n  poetry install\n  poetry build\n  cd dist\n  pip install *.whl\n\n',
    'author': 'ryanfeather',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
