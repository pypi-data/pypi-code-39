# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['xls2json']

package_data = \
{'': ['*']}

install_requires = \
['xlrd>=1.2,<2.0']

entry_points = \
{'console_scripts': ['xls2json = xls2json.command_line:main']}

setup_kwargs = {
    'name': 'xls2json',
    'version': '0.1.2',
    'description': 'Convert XLS file to JSON.',
    'long_description': "## xls2json\n\n```bash\nxls2json [--perentry] [--persheet] xls_input [output_path='output']\n```\n\nTake XLS file and write to JSON file(s) (single, one for every row, and/or one for every workbook sheet).\n\n### Requirements\n\n- xlrd\n\n### Installation\n\n```bash\npip3 install xls2json\n```\n\n## TODO\n\n- compatibility with json2xls\n\n\n<!-- [tbmreza-json2xls]() -->",
    'author': 'Reza Handzalah',
    'author_email': 'rezahandzalah@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
