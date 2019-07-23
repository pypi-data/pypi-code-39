# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aioapi', 'aioapi.inspect']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5.4', 'pydantic>=0.20.1']

setup_kwargs = {
    'name': 'aioapi',
    'version': '0.3.0a0',
    'description': 'Yet another way to build APIs using AIOHTTP framework',
    'long_description': '# aioapi\n\n[![Build Status](https://cloud.drone.io/api/badges/Gr1N/aioapi/status.svg)](https://cloud.drone.io/Gr1N/aioapi) [![codecov](https://codecov.io/gh/Gr1N/aioapi/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aioapi) ![PyPI](https://img.shields.io/pypi/v/aioapi.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aioapi.svg?label=pypi%20downloads) ![GitHub](https://img.shields.io/github/license/Gr1N/aioapi.svg)\n\nYet another way to build APIs using [`AIOHTTP`](https://aiohttp.readthedocs.io/) framework.\n\nFollow [documentation](https://gr1n.github.io/aioapi/) to know what you can do with `AIOAPI`.\n\n## Installation\n\n```sh\n$ pip install aioapi\n```\n\n## Usage & Examples\n\nBelow you can find a simple, but powerful example of `AIOAPI` library usage:\n\n```python\nimport aioapi as api\nfrom aioapi import Body, PathParam\nfrom aioapi.middlewares import validation_error_middleware\nfrom aiohttp import web\nfrom pydantic import BaseModel\n\n\nclass User(BaseModel):\n    name: str\n    age: int = 42\n\n\nasync def hello_body(user_id: PathParam[int], body: Body[User]):\n    user = body.cleaned\n    return web.json_response(\n        {"id": user_id.cleaned, "name": user.name, "age": user.age}\n    )\n\n\ndef main():\n    app = web.Application()\n\n    app.add_routes([api.post("/hello/{user_id}", hello_body)])\n    app.middlewares.append(validation_error_middleware)\n\n    web.run_app(app)\n\n\nif __name__ == "__main__":\n    main()\n```\n\nAnd there are also more examples of usage at [`examples/`](https://github.com/Gr1N/aioapi/tree/master/example) directory.\n\nTo run them use command below:\n\n```sh\n$ make example\n```\n\n## Contributing\n\nTo work on the `AIOAPI` codebase, you\'ll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):\n\n```sh\n$ git clone git@github.com:Gr1N/aioapi.git\n$ make install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ make lint && make test\n```\n\nIf you want to run only tests or linters you can explicitly specify what you want to run, e.g.:\n\n```sh\n$ make lint-black\n```\n\n## Milestones\n\nIf you\'re interesting in project\'s future you can find milestones and plans at [projects](https://github.com/Gr1N/aioapi/projects) page.\n\n## License\n\n`AIOAPI` is licensed under the MIT license. See the license file for details.\n',
    'author': 'Nikita Grishko',
    'author_email': 'gr1n@protonmail.com',
    'url': 'https://github.com/Gr1N/aioapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
