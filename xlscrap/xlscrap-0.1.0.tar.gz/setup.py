# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['xlscrap']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=2.6,<3.0']

setup_kwargs = {
    'name': 'xlscrap',
    'version': '0.1.0',
    'description': 'A package to ease Excel files mass data extraction',
    'long_description': "** WARNING : DON'T EXPECT SOMETHING USEFULL FROM THIS TOOL AT THIS STAGE !! **\n\n# xlscrap\n\nxlscrap is a [MIT-licensed](https://opensource.org/licenses/BSD-3-Clause) package to ease Excel files mass data extraction\n\nSee the [documentation](docs/index.md).\n\n# Rationale\n\nHave you ever feel the pain of extracting data from a lot of Excel files ?\n\n* When you have hundreds or thousands file that look similar\nbut differ in slighty annoying details.\n* When data cells coordinates can't be used because they change\n* When you have to spot dozens or hundreds fields with different strategies.\n* When the same field moves in different sheet position or name\n* When the same field label changes\n* When the data cell is on the right of the label or below the label\n* When you need to check that the collected data is correct.\n\nxlscrap helps you to scrap data out of your Excel files.\n\n# Quickstart\n\n```python\n>>> import xlscrap\n>>> s = xlscrap.Scrapper()\n>>> s.field('name')\n>>> s.field('age')\n>>> s.field('address')\n>>> s.table('pets', fields=['name', 'breed', 'age'])\n>>> s.scrap('excel-files/*.xls*')\nlooking for 4 fields in 5 files in excel-files/*.xls*,\nfile 1/5, found 4/4 fields in diana.xlsx\nfile 2/5, found 4/4 fields in bob.xls\nfile 3/5, found 3/4 fields in richard.ods\nfile 4/5, found 0/4 fields in alien.xls\nfile 5/5, found 4/4 fields in maria.xlsm\n>>> s.result\n[\n    {'name': 'Diana',\n    'age': 47,\n    'address': '44 rue du Louvre\\n75000 Paris\\nFrance'\n    'pets': []},\n    ...\n]\n```\n\n# TODO\n\n* set gitlab URL in setup.py\n* clone gitlab/github\n* complete quickstart in README\n  ",
    'author': 'Philippe ENTZMANN',
    'author_email': 'philippe@phec.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
