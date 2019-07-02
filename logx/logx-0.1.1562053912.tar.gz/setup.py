# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['logx', 'logxutil']

package_data = \
{'': ['*']}

install_requires = \
['logging_tree', 'pyyaml']

setup_kwargs = {
    'name': 'logx',
    'version': '0.1.1562053912',
    'description': 'best practice python logging with zero config',
    'long_description': '# logx: best practice python logging with zero config\n\nConfiguring logging is tedious. Reading the logging module docs makes me tired.\n\nWouldn\'t it be nice to log as easily as doing a print statement, without any upfront config?\n\n## Obligatory example\n\nEnter `logx`. It\'s as simple as:\n\n    >>> from logx import log\n    >>> log.info(\'hello world\')\n    hello world\n    >>> log.set_default_format()\n    >>> log.warn(\'warning!\')\n    [2018-02-26 21:51:16,971] WARNING [__main__.<module>:1] warning!\n\nLogs get logged automatically to the logger whose name matches the current module.\n\n## List of sweet features\n\n- Creates loggers lazily/as needed/on demand and **logs to the appropriate logger automatically**. If you\'re in the "acme" module it\'ll log to a log called "acme", no need worry about logger names and instances.\n- **Shows all log messages by default**, which follows the principle of least surprise and is probably what you want when debugging.\n- Included default handler **logs to the appropriate standard output stream by default**: Errors and warnings to stderr, the rest to stdout.\n- Allows easy following of best practice when including log statements in a library: **Just call log.create_null_handler() in your module.**\n- **Uses the standard logging library**, so you can still customize your setup as much as you want/need. Plays nicely with your existing logging config files.\n- **Includes the very useful logging_tree module** for viewing your current logging configuration. `logx.print_diagram()`\n\n## Install\n\n    >>> pip install logx\n\n## Contribute\n\nIssues and pull requests welcome, hit me. Am I doing logging completely wrong? Critique welcome, even if very pedantic.\n',
    'author': 'Robert Lechte',
    'author_email': 'robertlechte@gmail.com',
    'url': 'https://github.com/djrobstep/logx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
