# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['podcast_archiver']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=5.2,<6.0']

entry_points = \
{'console_scripts': ['podcast-archiver = podcast_archiver.__main__:main']}

setup_kwargs = {
    'name': 'podcast-archiver',
    'version': '1.0.0a0',
    'description': 'Feed parser and download client for local podcast archival',
    'long_description': None,
    'author': 'Jan Willhaus',
    'author_email': 'mail@janwillhaus.de',
    'url': 'https://github.com/janw/podcast-archiver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
