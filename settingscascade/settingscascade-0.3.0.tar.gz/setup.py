# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['settingscascade']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.10,<2.11', 'sortedcontainers>=2.1,<2.2']

setup_kwargs = {
    'name': 'settingscascade',
    'version': '0.3.0',
    'description': 'Cascade settings from multiple levels of specificity',
    'long_description': 'Intro\n======\n\nSettings cascade is designed for situations where you need to merge\nconfiguration settings from different hierarchical sources. The model\nis the way that CSS cascades onto elements. You can define config\nthe same way that css rules get specified-\n\n.. code-block:: yaml\n\n\ttask.default:\n\t    command: "echo hello"\n\t    on_complete: "echo world"\n\tproject_name: "my project"\n\nThen your app can use the config\n\n.. code-block:: python\n\n\tclass Task(SettingsSchema):\n\t\t_name_ = task\n\t\tcommand: str\n\t\ton_complete: str\n\n\tconfig = SettingsManager(yaml.load("config.yml"), [Task])\n\ttask_config = config.task(class="default")\n\trun_task(\n\t\tcommand=task_config.command,\n\t\ton_complete=task_config.on_complete,\n\t\tname=config.project_name,\n\t)\n\n\nInstallation\n==================\n\nYou can install settingscascade from pypi-\n\n::\n\n\tpip install settingscascade\n',
    'author': 'Paul Becotte',
    'author_email': 'pjbecotte@gmail.com',
    'url': 'https://gitlab.com/pjbecotte/settingscascade',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
