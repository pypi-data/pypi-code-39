# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ipython_namespaces']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=5.0,<6.0']

setup_kwargs = {
    'name': 'ipython-namespaces',
    'version': '0.1.2',
    'description': 'Extension for IPython/Jupyter Notebooks that adds namespaces that you can enter and re-enter',
    'long_description': "# IPython Namespaces\n\nExtension for IPython/Jupyter Notebooks that adds namespaces that you can enter and re-enter.\n\n(Because: “Namespaces are one honking great idea – let’s do more of those!”)\n\n## Usage (in a Jupyter Notebook)\n\nLoad the extension:\n\n```python\n%load_ext ipython-namespaces\n```\n\nUse the `space` cell magic:\n\n```\nfoo = 23\n```\n\n```\n%%space dustin\n\nbar = 42\nfoo, bar\n```\n\nOutput: `(23, 42)`\n\n```\nfoo, bar\n```\n\nOutput: `NameError: name 'bar' is not defined`\n\n```\n%%space dustin\n\nfoo, bar\n```\n\nOutput: `(23, 42)`\n\n```\nfrom ipython_namespaces import Namespaces\n\nNamespaces.dustin['bar']\n```\n\nOutput: `42`\n\n## Features\n\n1. Separate namespaces within one Jupyter Notebook\n2. Access to other namespaces via the `Namespaces` class\n3. Unchanged behavior of `display` – the value of the last line in a cell is displayed\n4. Unchanged behavior of tracebacks – the problematic line in one’s own code is highlighted\n\n## Acknowledgements\n\nThanks to Davide Sarra and the Jupyter Spaces extension for the inspiration!",
    'author': 'Denis Drescher',
    'author_email': 'denis.drescher@claviger.net',
    'url': 'https://bitbucket.org/Telofy/ipython-namespaces',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
