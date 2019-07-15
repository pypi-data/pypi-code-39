# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['snyksh']
install_requires = \
['ipython', 'prettyprinter', 'pysnyk', 'termcolor']

entry_points = \
{'console_scripts': ['snyksh = snyksh:run']}

setup_kwargs = {
    'name': 'snyksh',
    'version': '0.1.0',
    'description': 'An interactive shell interface for the Snyk API',
    'long_description': '# Snyk Shell\n\nSnyk Shell provides a convenient shell interface to the Snyk API. You can\nuse any valid Python expression as well as make calls to the Snyk API using\nthe pre-configured Snyk API client. When you load the the shell it will\npre-load a list of your organizations and projects so you have some data to explore.\n\n## Installation\n\nSnyk Shell is available from PyPi. Use your prefered Python dependency management tool to install:\n\n```\npip install snyksh\n```\n\nSnyk Shell is also available as a Docker image.\n\n```\ndocker pull garethr/snyksh\n```\n\n## Configuration\n\nIn order to access the Snyk API you need to provide your API token. This is done using\nan environment variable called `SNYK_TOKEN`:\n\n```\nexport SNYK_TOKEN=<your-token-goes-here>\nsnyksh\n```\n\n```\ndocker run --rm -it -e SNYK_TOKEN=<your-token> garethr/snyksh\n```\n\n## Usage\n\nWith Snyk Shell running you can interact with data in Snyk. This includes your projects as\nwell as vulnerability data more generally.\n\nHere\'s a few examples.\n\n```ipython\nWelcome to Snyk Shell\n\nThe following objects and methods are currently available:\n  client - An instance of the Snyk client, which can be used to make requests to the API\n  organizations - A prepopulated list of the Snyk organizations you are a member of\n  projects - A prepopulated list of all of your Snyk projects\n  pprint() - A pretty printer for objects returns by the API\n\n\nIn [1]: organizations\nOut[1]: [Organization(name=\'garethr\', id=\'<not-the-read-organization-id>\', group=None)]\n\nIn [2]: pprint(organizations)\n[\n    snyk.models.Organization(\n        name=\'garethr\',\n        id=\'<not-the-real-organization-id>\'\n    )\n]\n\nIn [3]: results = client.organizations.first().test_python("django", "2.0.0")\n\nIn [4]: len(results.issues.vulnerabilities)\nOut[4]: 6\n\nIn [5]: [x.identifiers["CVE"][0] for x in results.issues.vulnerabilities]\nOut[5]:\n[\'CVE-2019-6975\',\n \'CVE-2018-7536\',\n \'CVE-2018-7537\',\n \'CVE-2018-6188\',\n \'CVE-2018-14574\',\n \'CVE-2019-3498\']\n```\n\n## The Snyk API client\n\nSnyk Shell uses the Snyk Python API client `pysnyk`. If you want to build your own applications\nwhich interact with the Snyk API, or you want to know all of the properties and methods avaiable\nto you, see the client documentation and examples.\n\n\n',
    'author': 'Gareth Rushgrove',
    'author_email': 'gareth@morethanseven.net',
    'url': 'https://github.com/garethr/snyksh',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
