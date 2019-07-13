# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tefy']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.2.4,<5.0.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'tefy',
    'version': '0.1.4',
    'description': 'A very basic wrapper for conversions from doc, docx and odt to TEI XML',
    'long_description': "TEfy\n====\n\n|Build Status| |PyPI version| \n\n``TEfy`` was born out of the need to streamline the conversion of doc,\ndocx and odt documents into TEI XML when using Python scripts. It's a\nvery basic wrapper around the OxGarage_\nAPI at https://oxgarage.tei-c.org/ege-webservice/ and\ncovers a small subset of conversions, namely from doc, docx and odt to TEI\nXML. The conversion result is output as an lxml_ etree Element. \n\n.. _OxGarage: https://github.com/TEIC/oxgarage\n.. _lxml: https://github.com/lxml/lxml\n\nUsage \n-----\nYou can install TEfy with pip (``$ pip install TEfy``) \nand convert let's say an ODT document like this:\n\n.. code:: python\n\n    from tefy import OxGaWrap\n    doc = OxGaWrap('path/to/example.odt')\n    tei = doc.tei_xml\n\n.. |Build Status| image:: https://travis-ci.org/03b8/TEfy.svg?branch=master\n   :target: https://travis-ci.org/03b8/TEfy\n.. |PyPI version| image:: https://badge.fury.io/py/TEfy.svg\n   :target: https://badge.fury.io/py/TEfy\n",
    'author': 'Theo Costea',
    'author_email': 'theo.costea@gmail.com',
    'url': 'https://github.com/03b8/tefy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
