# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ocomone']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ocomone',
    'version': '0.3.1',
    'description': 'Common helper library by Anton Kachurin',
    'long_description': 'Set of common libraries by @outcatcher\n\n[ocomone](https://gitlab.com/outcatcher/ocomone/tree/master/ocomone) вЂ” library with most common functions, used by other libraries\n\n[ocomone-selene](https://gitlab.com/outcatcher/ocomone-selene) вЂ” set of features and whistles for selene+allure libraries\n\n[ocomone-pypi](https://gitlab.com/outcatcher/ocomone/tree/master/ocomone-pypi) вЂ” minimalistic pypi server setup based on\n[pypiserver](https://github.com/pypiserver/pypiserver) library\n',
    'author': 'Anton Kachurin',
    'author_email': 'katchuring@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
