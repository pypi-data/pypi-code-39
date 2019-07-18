# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['plx', 'plx.export']

package_data = \
{'': ['*']}

modules = \
['recparse']
install_requires = \
['attrs>=19.1,<20.0',
 'numpy>=1.16,<2.0',
 'pedroasad-attrs-patch>=0.2.1,<0.3.0',
 'pedroasad-marshmallow-patch>=0.1.1,<0.2.0',
 'pint>=0.9.0,<0.10.0']

extras_require = \
{'all': ['click>=7.0,<8.0'], 'cli': ['click>=7.0,<8.0']}

setup_kwargs = {
    'name': 'lcg-neuro-plx',
    'version': '0.1.0',
    'description': 'Parsing of PLX neurophysiological data files in Python',
    'long_description': "plx -- Parsing of PLX neurophysiological data files in Python\n=============================================================\n\n+-----------------------------------------------------------------------------------------------------------+\n| |badge-python-version| |badge-version|                                                                    | \n+-----------------------------------------------------------------------------------------------------------+\n| |badge-license| |badge-python-style|                                                                      |\n+-----------------------------------------------------------------------------------------------------------+\n| |badge-pipeline| |badge-security| |badge-codecov|                                                         |\n+-----------------------------------------------------------------------------------------------------------+\n| `Documentation <https://lcg.gitlab.io/neuro/python-plx>`__                                                |\n+-----------------------------------------------------------------------------------------------------------+\n| `Issue tracker <https://gitlab.com/lcg/neuro/python-plx/issues>`__                                        |\n+-----------------------------------------------------------------------------------------------------------+\n| `Repository contents <https://gitlab.com/lcg/neuro/python-plx/blob/master/MANIFEST.rst>`__                |\n+-----------------------------------------------------------------------------------------------------------+\n| `History of changes <https://gitlab.com/lcg/neuro/python-plx/blob/master/CHANGELOG.rst>`__                |\n+-----------------------------------------------------------------------------------------------------------+\n| `Contribution/development guide <https://gitlab.com/lcg/neuro/python-plx/blob/master/CONTRIBUTING.rst>`__ |\n+-----------------------------------------------------------------------------------------------------------+\n| `License <https://gitlab.com/lcg/neuro/python-plx/blob/master/LICENSE.txt>`__                             |\n+-----------------------------------------------------------------------------------------------------------+\n\n\nInstallation\n------------\n\n.. code:: bash\n\n    pip install lcg-neuro-plx\n\n\nUsage\n-----\n\nA minimal tutorial is pending.\nFor now, see the project's documentation at https://lcg.gitlab.io/neuro/python-plx.\n\n--------------\n\n- Powered by `GitLab CI <https://docs.gitlab.com/ee/ci>`__\n- Created by `Pedro Asad <pasad@lcg.ufrj.br> <mailto:pasad@lcg.ufrj.br>`__\n  using `cookiecutter <http://cookiecutter.readthedocs.io/>`__\n  and `@pedroasad.com/templates/python/python/app-1.0.0 <https://gitlab.com/pedroasad.com/templates/python/python-app/tags/1.0.0>`__\n\n.. |badge-python-version| image:: https://img.shields.io/badge/Python-%E2%89%A53.6-blue.svg\n   :target: https://docs.python.org/3.6\n\n.. |badge-version| image:: https://img.shields.io/badge/version-0.1.0%20-orange.svg\n   :target: https://test.pypi.org/project/lcg-neuro-plx/0.1.0/\n\n.. |badge-license| image:: https://img.shields.io/badge/license-MIT-blue.svg\n   :target: https://opensource.org/licenses/MIT\n\n.. |badge-python-style| image:: https://img.shields.io/badge/code%20style-Black-black.svg\n   :target: https://pypi.org/project/black/\n\n.. |badge-pipeline| image:: https://gitlab.com/lcg/neuro/python-plx/badges/master/pipeline.svg\n   :target: https://gitlab.com/lcg/neuro/python-plx\n\n.. |badge-security| image:: https://img.shields.io/badge/security-Check%20here!-yellow.svg\n   :target: https://gitlab.com/lcg/neuro/python-plx/security\n\n.. |badge-codecov| image:: https://codecov.io/gl/lcg:neuro/python-plx/branch/master/graph/badge.svg\n   :target: https://codecov.io/gl/lcg:neuro/python-plx\n",
    'author': 'Pedro Asad',
    'author_email': 'pasad@lcg.ufrj.br',
    'url': 'https://lcg.gitlab.io/neuro/python-plx',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}
from build_extensions import *
build(setup_kwargs)

setup(**setup_kwargs)
