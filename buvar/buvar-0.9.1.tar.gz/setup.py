# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['buvar', 'buvar.di', 'buvar.plugins']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'cattrs>=0.9.1,<0.10.0',
 'multidict>=4.5,<5.0',
 'orjson>=2.0,<3.0',
 'structlog>=19.1,<20.0',
 'toml>=0.10,<0.11',
 'tomlkit>=0.5.3,<0.6.0',
 'typing_inspect>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['buvar = buvar.cli:main']}

setup_kwargs = {
    'name': 'buvar',
    'version': '0.9.1',
    'description': 'General purpose asyncio service loader and dependency injector',
    'long_description': 'Búvár\n=====\n\nobjective\n---------\n\nBasically I want app similar, what `Pyramid`_ provides, but for asyncio\nand for a all kinds of services.\n\n* Have a plugin system, which runs code not on import time, but on run time. So\n  you can test and mock your code.\n\n* Have a component registry to hold certain state of your application.\n\n* Have a simple way to configure your application via OS environment.\n\n* Have always a structlog.\n\n.. _Pyramid: https://github.com/Pylons/pyramid\n\n\na use case\n----------\n\n`src/app/__main__.py`\n\n.. code-block:: python\n\n   """Main entry point to run the server."""\n   import asyncio\n   import os\n   import sys\n   import typing\n\n   import attr\n   import toml\n   import structlog\n\n   from buvar import components, config, log, plugin\n\n\n   @attr.s(auto_attribs=True)\n   class GeneralConfig:\n       """Simple config."""\n\n       log_level: str = "INFO"\n       plugins: typing.Set[str] = set()\n\n\n   loop = asyncio.get_event_loop()\n   user_config = toml.load(\n       os.environ.get("USER_CONFIG", os.path.dirname(__file__) + "/user_config.toml")\n   )\n\n   cmps = components.Components()\n   source = cmps.add(config.ConfigSource(user_config, env_prefix="APP"))\n   general_config = cmps.add(source.load(GeneralConfig))\n\n   log.setup_logging(sys.stdout.isatty(), general_config.log_level)\n\n   sl = structlog.get_logger()\n   sl.info("Starting process", pid=os.getpid())\n   sl.debug("Config used", **source)\n\n   plugin.run(*general_config.plugins, components=cmps, loop=loop)\n\n\n`src/app/user_config.toml`\n\n.. code-block:: toml\n\n   log_level = "DEBUG"\n   plugins = [\'app\']\n\n   [aiohttp]\n   host = "127.0.0.1"\n   port = 5000\n\n\n\n`src/app/__init__.py`\n\n.. code-block:: python\n\n   import aiohttp.web\n   import structlog\n\n   from buvar import context\n\n   log = structlog.get_logger()\n   routes = aiohttp.web.RouteTableDef()\n\n\n   @routes.get("/")\n   async def index(request):\n       return aiohttp.web.json_response({"hello": "world"})\n\n\n   async def plugin(include):\n       await include(".server")\n       app = context.get(aiohttp.web.Application)\n       app.add_routes(routes)\n\n`src/app/server.py`\n\n.. code-block:: python\n\n   """Create a aiohttp server task and provide the application via context."""\n   import aiohttp.web\n   import attr\n   import structlog\n\n   from buvar import config, context\n\n   sl = structlog.get_logger()\n\n\n   @attr.s(auto_attribs=True)\n   class AioHttpConfig:\n       host: str = "0.0.0.0"\n       port: int = 8080\n\n\n   class AccessLogger(aiohttp.abc.AbstractAccessLogger):  # noqa: R0903\n       def log(self, request, response, time):  # noqa: R0201\n           sl.info(\n               "Access",\n               remote=request.remote,\n               method=request.method,\n               path=request.path,\n               time=time,\n               status=response.status,\n           )\n\n\n   async def plugin():\n       config_source = context.get(config.ConfigSource)\n       aiohttp_config = config_source.load(AioHttpConfig, "aiohttp")\n       aiohttp_app = context.add(\n           aiohttp.web.Application(middlewares=[aiohttp.web.normalize_path_middleware()])\n       )\n\n       sl.info("Running web server", host=aiohttp_config.host, port=aiohttp_config.port)\n       # return server task\n       yield aiohttp.web._run_app(  # noqa: W0212\n           aiohttp_app, host=aiohttp_config.host, port=aiohttp_config.port, print=None\n       )\n\n\n\n\n.. code-block:: bash\n\n   cd src\n   APP_AIOHTTP_HOST=0.0.0.0 APP_AIOHTTP_PORT=8080 python -m app\n\n.. code-block::\n\n   2019-07-09T20:52:40.979551Z [info     ] Starting process               [__main__] pid=13158\n   2019-07-09T20:52:40.979753Z [debug    ] Config used                    [__main__] aiohttp={\'host\': \'127.0.0.1\', \'port\': 5000} log_level=DEBUG pid=13158 plugins=[\'app\']\n   2019-07-09T20:52:40.980269Z [debug    ] Using selector: EpollSelector  [asyncio] pid=13158\n   2019-07-09T20:52:40.981489Z [info     ] Running web server             [app.server] host=0.0.0.0 pid=13158 port=8080\n',
    'author': 'Oliver Berger',
    'author_email': 'diefans@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
