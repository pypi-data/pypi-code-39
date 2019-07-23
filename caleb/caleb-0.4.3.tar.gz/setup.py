# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['caleb', 'caleb.bin']

package_data = \
{'': ['*']}

install_requires = \
['crossref-commons>=0.0.5,<0.0.6']

entry_points = \
{'console_scripts': ['caleb = caleb.bin.caleb:main']}

setup_kwargs = {
    'name': 'caleb',
    'version': '0.4.3',
    'description': 'A tool to automatically retrieve bibtex entries',
    'long_description': "# caleb\n\n[![PyPI version](https://badge.fury.io/py/caleb.svg)](https://badge.fury.io/py/caleb)\n[![Coverage Status](https://coveralls.io/repos/github/kevinywlui/caleb/badge.svg)](https://coveralls.io/github/kevinywlui/caleb)\n[![Build Status](https://travis-ci.org/kevinywlui/caleb.svg?branch=master)](https://travis-ci.org/kevinywlui/caleb)\n\n**caleb** is a tool to automatically fill in your Latex citations.\n\n## Usage examples\n\nSee the `examples` directory along with the `an_example.tex` file. The\nfollowing examples occur in the `examples` directory.\n\n* The best way is probably to integrate into `latexmk`. The `-pdflatex` flag\n  allows us to run `caleb` after each `pdflatex` call.\n```\nlatexmk -pdf -pdflatex='pdflatex %O %S; caleb %B' an_example\n```\n\n* We can set the `-pdflatex` flag in a `.latexmkrc` file. This can either go in\n  the your tex project folder or in the home directory. So in the `.latexmkrc`\n  file, include the following line (see examples directory for an example):\n```\n$pdflatex='pdflatex %O %S; caleb %B'\n``` \n\n* The barebone approach is to run `caleb` before running bibtex.\n```\npdflatex an_example\ncaleb an_example\nbibtex an_example\npdflatex an_example\npdflatex an_example\n```\n\n* By default, `caleb` will ignore any citation where crossref.org returns\n  multiple results. To take the first result ordered by relevance, pass the\n  `--take-first` flag. For example,\n```\ncaleb --take-first an_example\n```\n\n\n\n## Installation\n\n### Dependencies\n\n* [crossref_commons_py](https://gitlab.com/crossref/crossref_commons_py)\n* `python3`\n\n### Testing and Development Dependencies\n\n* [python-coveralls](https://github.com/z4r/python-coveralls)\n* [pytest](https://pytest.org/en/latest/) \n* [pytest-cov](https://github.com/pytest-dev/pytest-cov)\n* [flake8](http://flake8.pycqa.org/en/latest/)\n\n### `setup.py`\n\n```\npython setup.py install --user\n```\n\n### `pip`\n\n```\npip3 install caleb --user\n```\n\n## Goal of project\n\n* [ ] Reach feature parity with IRL [Caleb](https://sites.math.washington.edu/~geigerc/)\n\n## Homepage\n\n* https://github.com/kevinywlui/caleb\n",
    'author': 'kevin lui',
    'author_email': 'kevinywlui@gmail.com',
    'url': 'https://github.com/kevinywlui/caleb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
