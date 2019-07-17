# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['marshmallow_patch', 'marshmallow_patch.marshmallow']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=2.19,<3.0', 'marshmallow_annotations>=2.4,<3.0']

extras_require = \
{'all': ['numpy>=1.16,<2.0', 'pint>=0.9.0,<0.10.0'],
 'numpy': ['numpy>=1.16,<2.0'],
 'pint': ['pint>=0.9.0,<0.10.0']}

setup_kwargs = {
    'name': 'pedroasad-marshmallow-patch',
    'version': '0.1.0',
    'description': 'A set of patches to the excellect marshmallow library',
    'long_description': '# marshmallow-patch &ndash; A set of patches to the excellent [Marshmallow] library\n\n[![][badge-python]][python-docs]\n[![][badge-version]][repository-latest-release]\n\n[![][badge-mit]][MIT License]\n[![][badge-black]][Black]\n\n[![][badge-ci-status]][repository-master]\n[![][badge-ci-security]][repository-security]\n[![][badge-codecov]][repository-codecov]\n\nFor | See\n--- | ---\nDocumentation | https://psa-exe.gitlab.io/python-marshmallow-patch\nIssue tracker | https://gitlab.com/psa-exe//python-marshmallow-patch/issues\nRepository contents | [MANIFEST]\nHistory of changes | [CHANGELOG]\nContribution/development guide | [CONTRIBUTING]\nCopy of [MIT License] | [LICENSE]\n\n---\n\n## Installation\n\n```bash\npip install pedroasad-marshmallow-patch\n```\n\nThis library contains optional support for [Numpy] arrays and [Pint] physical units and quantities.\nThese may be installed by passing the `[numpy]`, `[pint]`, or `[all]` options when installing.\n\n## Usage\n\nIt acts as a drop-in replacement to [Marshmallow]:\n\n```python\nfrom marshmallow_patch import marshmallow \n```\n\nFurther configuration may be performed by setting up global variables in [marshmallow_patch.config](https://psa-exe.gitlab.io/python-marshmallow-patch/api.html#module-marshmallow_patch.config) prior to importing the module replacement.\nOther [Marshmallow] sub-modules may be imported directly from the original package.\n\n---\n\n*&mdash; Powered by [GitLab CI]*  \n*&mdash; Created by Pedro Asad\n[&lt;pasad@lcg.ufrj.br&gt;](mailto:pasad@lcg.ufrj.br) using [cookiecutter] and [@pedroasad.com/templates/python/python/app-1.0.0](https://gitlab.com/pedroasad.com/templates/python/python-app/tags/1.0.0)*  \n\n[Black]: https://pypi.org/project/black/\n[CHANGELOG]: ./CHANGELOG.md\n[CONTRIBUTING]: ./CONTRIBUTING.md\n[Gitlab CI]: https://docs.gitlab.com/ee/ci\n[LICENSE]: ./LICENSE.txt\n[MANIFEST]: ./MANIFEST.md\n[MIT License]: https://opensource.org/licenses/MIT\n[Numpy]: https://www.numpy.org/\n[Pint]: https://pint.readthedocs.io/\n[README]: https://gitlab.com/psa-exe//python-marshmallow-patch/blob/master/README.md\n[TestPyPI]: https://test.pypi.org/\n[badge-black]: https://img.shields.io/badge/code%20style-Black-black.svg\n[badge-ci-coverage]: https://gitlab.com/psa-exe//python-marshmallow-patch/badges/master/coverage.svg\n[badge-ci-security]: https://img.shields.io/badge/security-Check%20here!-yellow.svg\n[badge-ci-status]: https://gitlab.com/psa-exe//python-marshmallow-patch/badges/master/pipeline.svg\n[badge-codecov]: https://codecov.io/gl/psa-exe/python-marshmallow-patch/branch/master/graph/badge.svg\n[badge-mit]: https://img.shields.io/badge/license-MIT-blue.svg\n[badge-python]: https://img.shields.io/badge/Python-%E2%89%A53.6-blue.svg\n[badge-version]: https://img.shields.io/badge/version-0.1.0%20alpha-orange.svg\n[cookiecutter]: http://cookiecutter.readthedocs.io/\n[Marshmallow]: https://marshmallow.readthedocs.io/en/3.0/\n[python-docs]: https://docs.python.org/3.6\n[repository-codecov]: https://codecov.io/gl/psa-exe/python-marshmallow-patch\n[repository-latest-release]: https://test.pypi.org/project/marshmallow-patch/0.1.0/\n[repository-master]: https://gitlab.com/psa-exe//python-marshmallow-patch\n[repository]: https://gitlab.com/psa-exe//python-marshmallow-patch\n[repository-security]: https://gitlab.com/psa-exe//python-marshmallow-patch/security\n\n',
    'author': 'Pedro Asad',
    'author_email': 'pasad@lcg.ufrj.br',
    'url': 'https://psa-exe.gitlab.io/python-marshmallow-patch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
