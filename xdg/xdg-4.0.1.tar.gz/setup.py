# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['xdg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xdg',
    'version': '4.0.1',
    'description': 'Variables defined by the XDG Base Directory Specification',
    'long_description': '# xdg\n\n`xdg` is a tiny Python module which provides the variables defined by the [XDG\nBase Directory Specification][spec], to save you from duplicating the same\nsnippet of logic in every Python utility you write that deals with user cache,\nconfiguration, or data files. It has no external dependencies.\n\n## Installation\n\nTo install the latest release from [PyPI], use [pip]:\n\n```bash\npip install xdg\n```\n\nIn Python projects using [Poetry] or [Pipenv] for dependency management, add\n`xdg` as a dependency with `poetry add xdg` or `pipenv install xdg`.\nAlternatively, since `xdg` is only a single file you may prefer to just copy\n`src/xdg/__init__.py` from the source distribution into your project.\n\n## Usage\n\n```python\nfrom xdg import (XDG_CACHE_HOME, XDG_CONFIG_DIRS, XDG_CONFIG_HOME,\n                 XDG_DATA_DIRS, XDG_DATA_HOME, XDG_RUNTIME_DIR)\n```\n\n`XDG_CACHE_HOME`, `XDG_CONFIG_HOME`, and `XDG_DATA_HOME` are [`pathlib.Path`\nobjects][path] containing the value of the environment variable of the same\nname, or the default defined in the specification if the environment variable is\nunset or empty.\n\n`XDG_CONFIG_DIRS` and `XDG_DATA_DIRS` are lists of `pathlib.Path` objects\ncontaining the value of the environment variable of the same name split on\ncolons, or the default defined in the specification if the environment variable\nis unset or empty.\n\n`XDG_RUNTIME_DIR` is a `pathlib.Path` object containing the value of the\nenvironment variable of the same name, or `None` if the environment variable is\nunset.\n\n## Copyright\n\nCopyright © 2016-2019 [Scott Stevenson].\n\n`xdg` is distributed under the terms of the [ISC licence].\n\n[isc licence]: https://opensource.org/licenses/ISC\n[path]: https://docs.python.org/3/library/pathlib.html#pathlib.Path\n[pip]: https://pip.pypa.io/en/stable/\n[pipenv]: https://docs.pipenv.org/\n[poetry]: https://poetry.eustace.io/\n[pypi]: https://pypi.org/project/xdg/\n[scott stevenson]: https://scott.stevenson.io\n[spec]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html\n',
    'author': 'Scott Stevenson',
    'author_email': 'scott@stevenson.io',
    'url': 'https://github.com/srstevenson/xdg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
