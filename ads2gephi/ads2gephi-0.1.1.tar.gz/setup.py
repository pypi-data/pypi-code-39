# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ads2gephi']

package_data = \
{'': ['*']}

install_requires = \
['ads>=0.12.3,<0.13.0',
 'click>=7.0,<8.0',
 'configparser>=3.7,<4.0',
 'hypothesis>=4.28,<5.0',
 'igraph>=0.1.11,<0.2.0',
 'pytest>=5.0,<6.0',
 'sqlalchemy>=1.3,<2.0']

entry_points = \
{'console_scripts': ['ads2gephi = ads2gephi.cli:main']}

setup_kwargs = {
    'name': 'ads2gephi',
    'version': '0.1.1',
    'description': 'A command line tool for querying and modeling citation networks from the Astrophysical Data System (ADS) in a format compatible with Gephi',
    'long_description': "# ads2gephi\n\nis a command line tool for querying and modeling citation networks from the Astrophysical Data System (ADS) in a format compatible with Gephi, a popular network visualization tool. ads2gephi has been developed at the history of science department of TU Berlin as part of a research project on the history of extragalactic astronomy.\n\n### Usage\n\nWhen using the tool for the first time to model a network, you will be prompted to enter your ADS API key. Your key will then be stored in a configuration file under ~/.ads2gephi.\n\nIn order to sample an initial citation network, you need to provide ads2gephi with a plain text file with bibcodes (ADS unique identifiers), one per line, as input. The queried network will be output in a SQLite database stored in the current directory:\n\n```\nads2gephi -c bibcodes_example.txt -d my_fancy_netzwerk.db\n```\n\nAfterwards you can extend the queried network by providing the existing database file and using the additional sampling options. For example, you can extend the network by querying all the items cited in every publication previously queried:\n\n```\nads2gephi -s ref -d network_database_example.db \n```\n\nFinally you might want to also generate the edges of the network. There are several options for generating edges. For example you can use a semantic similarity measure like bibliographic coupling or co-citation:\n```\nads2gephi -e bibcp -d network_database_example.db\n```\n\nAll other querying and modelling options are described in the help page:\n```\nads2gephi -h\n```\n\nOnce you're finished querying and modeling, fhe database file can be directly imported in Gephi for network visualization and analysis.\n\n## Special thanks to\n\n* Edwin Henneken\n",
    'author': 'Theo Costea',
    'author_email': 'theo.costea@gmail.com',
    'url': 'https://github.com/03b8/ads2gephi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
