# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dj_pony', 'dj_pony.django_docker_test_dbs']

package_data = \
{'': ['*'],
 'dj_pony.django_docker_test_dbs': ['static/css/*',
                                    'static/img/*',
                                    'static/js/*',
                                    'templates/dj_pony_docker_test_dbs/*']}

install_requires = \
['docker>=4.0,<5.0']

setup_kwargs = {
    'name': 'dj-pony.django-docker-test-dbs',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Samuel Bishop',
    'author_email': 'sam@techdragon.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
