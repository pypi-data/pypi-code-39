# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['moralizer']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=2.1,<3.0']

setup_kwargs = {
    'name': 'moralizer',
    'version': '0.1.4',
    'description': '> Simple tool to get the Moral Foundations counts of a given text.',
    'long_description': '# Moralizer\n> Simple tool to get the Moral Foundations counts of a given text. \n\n![MIT](https://img.shields.io/dub/l/vibe-d.svg?style=flat-square)\n![dependencies](https://img.shields.io/david/expressjs/express.svg?style=flat-square)\n![python](https://img.shields.io/badge/python-3.6%2C3.7-blue.svg?style=flat-square)\n\n## Installation\n```shell\npip install moralizer\n```\nSpaCy requires the following add-on.\n```shell\npython -m spacy download en_core_web_sm\n```\n## Description \nMoralizer returns word counts of a text based on the [Moral Foundations Vocabulary 2.0](https://osf.io/ezn37/) in a neat and organized JSON object or Python dictionary.\n\n## Use\n\n```python\nfrom moralizer import *\n```\n- moralizer\n  - read_json(reads in a json file)\n  - read_file(input_file)\n  - moralize(text, output_format=default is Python dictionary, add ".json" for output in JSON).\n\n\n## Dependencies\nMoralizer only uses one outside dependency, the delightfully opinionated [**spaCy**](https://spacy.io/).\n\n## Under Construction \n- Tests\n- Documentation',
    'author': 'npm',
    'author_email': None,
    'url': 'https://github.com/npmontgomery/moralizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
