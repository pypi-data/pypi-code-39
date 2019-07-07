# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fhir_tools']

package_data = \
{'': ['*'], 'fhir_tools': ['definitions/v4/generated/*']}

install_requires = \
['six']

setup_kwargs = {
    'name': 'fhir-tools',
    'version': '0.1.1',
    'description': 'Toolbox for working with FHIR Resources and Types',
    'long_description': "# fhir_tools\n\nSimple set of tools for working with FHIR resources and complex types.\n\nBasic usage:\n\n```python\nfrom fhir_tools import readers\nfrom fhir_tools import resources\n\ndefinitions = readers.defs_from_generated()\nresources = resources.Resources(definitions)\n\nname = resources.HumanName(family='Doe', given=['John'], text='John Doe')\npatient = resource.Patient(name=[name], id='example')\n\nprint(patient.name[0].text)\n```\n",
    'author': "Pavel 'Blane' Tuchin",
    'author_email': 'blane.public@gmail.com',
    'url': 'https://github.com/blanebf/fhir_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
