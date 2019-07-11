# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['autopub']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.5.5,<0.6.0']

extras_require = \
{'github': ['githubrelease>=1.5.8,<2.0.0']}

entry_points = \
{'console_scripts': ['autopub = autopub.autopub:main']}

setup_kwargs = {
    'name': 'autopub',
    'version': '0.1.0a9',
    'description': 'Automatic package release upon pull request merge',
    'long_description': '# AutoPub\n\nAutoPub enables project maintainers to release new package versions to PyPI by merging pull requests.\n\n## Environment\n\nAutoPub is intended for use with continuous integration (CI) systems and currently supports CircleCI. Projects used with AutoPub are assumed to be managed via [Poetry][].Support for other CI and build systems is planned and contributions adding such support would be welcome.\n\n## Configuration\n\nAutoPub settings can be configured via the `[tool.autopub]` table in the target project’s `pyproject.toml` file. Required settings include Git username and email address:\n\n```toml\n[tool.autopub]\ngit-username = "Your Name"\ngit-email = "your_email@example.com"\n```\n\n## Release Files\n\nContributors should include a `RELEASE.md` file in their pull requests with two bits of information:\n\n* Release type: major, minor, or patch\n* Description of the changes, to be used as the changelog entry\n\nExample:\n\n    Release type: patch\n\n    Add function to update version strings in multiple files.\n\n## Usage\n\nThe following `autopub` sub-commands can be used as steps in your CI flows:\n\n* `autopub check`: Check whether release file exists.\n* `autopub prepare`: Update version strings and add entry to changelog.\n* `autopub commit`: Add, commit, and push incremented version and changelog changes.\n* `autopub githubrelease`: Create a new release on GitHub.\n\n\n[Poetry]: https://poetry.eustace.io\n',
    'author': 'Justin Mayer',
    'author_email': 'entrop@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
