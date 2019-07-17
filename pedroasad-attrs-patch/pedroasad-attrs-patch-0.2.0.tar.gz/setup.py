# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['attrs_patch', 'attrs_patch.attr']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0']

extras_require = \
{'all': ['numpy>=1.16,<2.0'], 'numpy': ['numpy>=1.16,<2.0']}

setup_kwargs = {
    'name': 'pedroasad-attrs-patch',
    'version': '0.2.0',
    'description': 'A set of patches for the excellent attrs library',
    'long_description': '# Python application template\n\n[![][badge-python]][python-docs]\n[![][badge-version]][repository-latest-release]\n\n[![][badge-mit]][MIT License]\n[![][badge-black]][Black] + [![][badge-flake8]][flake8]\n\n[![][badge-ci-status]][repository-master]\n[![][badge-ci-security]][repository-security]\n[![][badge-codecov]][repository-codecov]\n\n*A set of patches for the excellent attrs library*\n\n| For                            | See                                                  |\n| ------------------------------ | ---------------------------------------------------- |\n| Documentation                  | https://psa-exe.gitlab.io/python-attrs-patch         |\n| Issue tracker                  | https://gitlab.com/psa-exe/python-attrs-patch/issues |\n| Repository contents            | [MANIFEST]                                           |\n| History of changes             | [CHANGELOG]                                          |\n| Contribution/development guide | [CONTRIBUTING]                                       |\n| Copy of [MIT License]          | [LICENSE]                                            |\n\n---\n\n## Installation\n\n```bash\npip install pedroasad-attrs-patch\n```\n\nThis library contains optional support for [Numpy] arrays in [attrs frozen classes](http://www.attrs.org/en/stable/how-does-it-work.html?highlight=frozen#immutability).\nIt may be installed by passing the `[numpy]` option when installing.\n\n\n## Usage\n\nIt acts as a drop-in replacement to [attrs].\nThe example below shows how to use it, including all currently existing improvements.\n\n```python\nfrom attrs_patch import attr\n\n\n@attr.autodoc\n@attr.s(frozen=True)\nclass SomeClass:\n    a = attr.ib(metadata={"help": "An immutable numpy array."}, \n                converter=attr.frozen_numpy_array,\n                hash=False)\n    b = attr.ib(metadata={"help": "A positive integer."},\n                converter=int,\n                validator=attr.validators.positive)\n    c = attr.ib(metadata={"help": "A non-zero integer."}, \n                converter=int,\n                validator=attr.validators.nonzero)\n```\n\n---\n\n*&mdash; Powered by [GitLab CI]*  \n*&mdash; Created by [Pedro Asad &lt;pasad@lcg.ufrj.br&gt;](mailto:pasad@lcg.ufrj.br) using [cookiecutter] and [@pedroasad.com/templates/python/python-app-1.0](https://gitlab.com/pedroasad.com/templates/python/python-app/tags/1.0.0)*\n\n[Black]: https://black.readthedocs.io/en/stable/\n[CHANGELOG]: ./CHANGELOG.md\n[CONTRIBUTING]: ./CONTRIBUTING.md\n[Gitlab CI]: https://docs.gitlab.com/ee/ci\n[LICENSE]: ./LICENSE.txt\n[MANIFEST]: ./MANIFEST.md\n[MIT License]: https://opensource.org/licenses/MIT\n[Numpy]: https://www.numpy.org/\n[README]: https://gitlab.com/psa-exe/python-attrs-patch/blob/master/README.md\n[TestPyPI]: https://test.pypi.org/\n[attrs]: https://www.attrs.org\n[autopep8]: https://pypi.org/project/autopep8/\n[badge-black]: https://img.shields.io/badge/code%20style-Black-black.svg\n[cookiecutter]: https://cookiecutter.readthedocs.io\n[badge-ci-coverage]: https://gitlab.com/psa-exe/python-attrs-patch/badges/master/coverage.svg\n[badge-ci-security]: https://img.shields.io/badge/security-Check%20here!-yellow.svg\n[badge-ci-status]: https://gitlab.com/psa-exe/python-attrs-patch/badges/master/pipeline.svg\n[badge-codecov]: https://codecov.io/gl/psa-exe/python-attrs-patch/branch/master/graph/badge.svg\n[badge-flake8]: https://img.shields.io/badge/code%20style-Flake8-blue.svg\n[badge-mit]: https://img.shields.io/badge/license-MIT-blue.svg\n[badge-python]: https://img.shields.io/badge/Python-%E2%89%A53.6-blue.svg\n[badge-version]: https://img.shields.io/badge/version-0.2.0%20(alpha)-orange.svg\n[flake8]: http://flake8.pycqa.org/en/latest/\n[python-docs]: https://docs.python.org/3.5\n[repository-codecov]: https://codecov.io/gl/psa-exe/python-attrs-patch\n[repository-latest-release]: https://test.pypi.org/project/attrs-patch/0.2.0/\n[repository-master]: https://gitlab.com/psa-exe/python-attrs-patch\n[repository-security]: https://gitlab.com/psa-exe/python-attrs-patch/security\n[repository]: https://gitlab.com/psa-exe/python-attrs-patch\n\n',
    'author': 'Pedro Asad',
    'author_email': 'pasad@lcg.ufrj.br',
    'url': 'https://psa-exe.gitlab.io/python-attrs-patch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
