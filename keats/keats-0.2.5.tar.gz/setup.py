# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keat_scripts', 'keats']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.1.3,<0.2.0', 'termcolor>=1.1,<2.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['keats = keats:main']}

setup_kwargs = {
    'name': 'keats',
    'version': '0.2.5',
    'description': 'Utilities for managing version, changelogs, and project releases.',
    'long_description': '# Keats\n\n![John Keats](assets/keats.jpg)\n\nKeats is an utilities package for poetry.\n\nFeatures include forced change logs, release scripts, and package version control.\n\n## Usage\n\n```\nkeats bump <VERSION>\n```\n\n```\n# get the package version number\nkeats version\n```\n\n## Installation\n\n\n```\n# globally install keats\npip install keats\n```\n\n```\n# locally install keats\npoetry add --dev keats\n\n# run keats\npoetry run keats\n```',
    'author': 'jvrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': 'https://github.com/jvrana/keats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
