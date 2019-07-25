# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['context_logging']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'context-logging',
    'version': '0.2.0',
    'description': 'Tool for easy logging with current context information',
    'long_description': "# context_logging\n\n[![pypi](https://badge.fury.io/py/context_logging.svg)](https://pypi.org/project/context_logging)\n[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://pypi.org/project/context_logging)\n[![Downloads](https://img.shields.io/pypi/dm/context_logging.svg)](https://pypistats.org/packages/context_logging)\n[![Build Status](https://travis-ci.org/Afonasev/context_logging.svg?branch=master)](https://travis-ci.org/Afonasev/context_logging)\n[![Code coverage](https://codecov.io/gh/Afonasev/context_logging/branch/master/graph/badge.svg)](https://codecov.io/gh/Afonasev/context_logging)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n## Description\n\nTool for easy logging with current context information\n\n## Installation\n\n    pip install context_logging\n\n## Usage\n\n### As contextmanager\n\n```python\nfrom context_logging import Context, current_context\n\nwith Context(val=1):\n    assert current_context['val'] == 1\n\nassert 'val' not in current_context\n```\n\n### Any nesting of contexts is allowed\n\n```python\nwith Context(val=1):\n    assert current_context == {'val': 1}\n\n    with Context(val=2, var=2):\n        assert current_context == {'val': 2, 'var': 2}\n\n    assert current_context == {'val': 1}\n\nassert 'val' not in current_context\n```\n\n### As decorator\n\n```python\n@Context(val=1)\ndef f():\n    assert current_context['val'] == 1\n\nf()\nassert 'val' not in current_context\n```\n\n### With start/finish\n\n```python\nctx = Context(val=1)\nassert 'val' not in current_context\n\nctx.start()\nassert current_context['val'] == 1\n\nctx.finish()\nassert 'val' not in current_context\n```\n\n### Write/delete to current_context\n```python\nwith Context():\n    assert 'val' not in current_context\n    current_context['val'] = 1\n    assert current_context['val'] == 1\n```\n\n### Explicit context name (else will be used path to the python module)\n\n```python\nwith Context(name='my_context'):\n    pass\n```\n\n### Setup logging with context\n\n```python\nimport logging\nfrom context_logging import current_context, setup_log_record\n\nlogging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s %(context)s', level=logging.INFO)\nsetup_log_record()\n\ncurrent_context['val'] = 1\nlogging.info('message')\n\n# 2019-07-25 19:49:43,892 INFO root message {'val': 1}\n```\n\n### Execution time logged on exit from context (disable with `log_execution_time=False`)\n\n```python\nwith Context(name='my_context'):\n    time.sleep(1)\n\n# INFO 'my_context: executed in 00:00:01',\n```\n\n### Exceptions from context are populated with current_contextdisable with `fill_exception_context=False`)\n\n```python\ntry:\n    with Context(val=1):\n        raise Exception(1)\nexcept Exception as exc:\n    assert exc.args = (1, {'val': 1})\n```\n\n### We can set data to root context that never will be closed\n\n```python\nfrom context_logging import root_context\n\nroot_context['env'] = 'test'\n```\n\n### For autofilling thread context in async code\n\n```python\nfrom contextvars_executor import ContextVarExecutor\n\nloop.set_default_executor(ContextVarExecutor())\n```\n\n## For developers\n\n### Create venv and install deps\n\n    make init\n\n### Install git precommit hook\n\n    make precommit_install\n\n### Run linters, autoformat, tests etc.\n\n    make pretty lint test\n\n### Bump new version\n\n    make bump_major\n    make bump_minor\n    make bump_patch\n\n## License\n\nMIT\n\n## Change Log\n\nUnreleased\n-----\n\n* ...\n\n0.2.0 - 2019-07-25\n-----\n\n* context as attr of log record\n\n0.1.0 - 2019-07-23\n-----\n\n* initial\n",
    'author': 'Evgeniy Afonasev',
    'author_email': 'ea.afonasev@gmail.com',
    'url': 'https://pypi.org/project/context_logging',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
