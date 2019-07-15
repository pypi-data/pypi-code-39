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
 'cattrs>=0.9.0,<0.10.0',
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
    'version': '0.10.0',
    'description': 'General purpose asyncio service loader and dependency injector',
    'long_description': 'Búvár\n=====\n\na plugin mechanic\n-----------------\n\nI want to have a plugin mechanic similar to `Pyramid`_\\\'s aproach. It should\nprovide means to spawn arbitrary tasks to run, where every lifecycle stage\nshould be yielded to the developer control.\n\nYou bootstrap like following:\n\n.. code-block:: python\n\n    from buvar import plugin, components\n\n    plugin.run("some.module.with.plugin.function")\n\n\n.. code-block:: python\n\n   # some.module.with.plugin.function\n   from buvar import context\n\n\n   # you may omit include in arguments\n   async def plugin(include):\n      await include(\'.another.plugin\')\n\n      # create some long lasting components\n      my_component = context.add("some value")\n\n      async def task():\n         asyncio.sleep(1)\n\n      async def server():\n         await asyncio.Future()\n\n      # you may run simple tasks\n      yield task()\n\n      # you may run server tasks\n      yield server()\n\n\na components and dependency injection solution\n----------------------------------------------\n\nI want to have some utility to store some long lasting means of aid to my\nbusiness problem. I want a non-verbose lookup to those.\n\n.. code-block:: python\n\n   from buvar import di\n\n   class Bar:\n      pass\n\n   class Foo:\n      def __init__(self, bar: Bar = None):\n         self.bar = bar\n\n      @di.register\n      async def adapt(cls, baz: str) -> Foo:\n         return Foo()\n\n   @di.register\n   async def adapt(bar: Bar) -> Foo\n      foo = Foo(bar)\n      return foo\n\n\n   async def task():\n      foo = await di.nject(Foo, baz="baz")\n      assert foo.bar is None\n\n      bar = Bar()\n      foo = await di.nject(Foo, bar=bar)\n      assert foo.bar is bar\n\n\na config source\n---------------\n\nI want to have a config source, which automatically applies environment\nvariables to the defaults.\n\n`config.toml`\n\n.. code-block:: toml\n\n   log_level = "DEBUG"\n   show_warnings = "yes"\n\n   [foobar]\n   some = "value"\n\n\n.. code-block:: bash\n\n   export APP_FOOBAR_SOME=thing\n\n\n.. code-block:: python\n\n   import attr\n   import toml\n\n   from buvar import config\n\n   @attr.s(auto_attribs=True)\n   class GeneralConfig:\n       log_level: str = "INFO"\n       show_warnings: bool = config.bool_var(False)\n\n   @attr.s(auto_attribs=True)\n   class FoobarConfig:\n      some: str\n\n   source = config.ConfigSource(toml.load(\'config.toml\'), env_prefix="APP")\n\n   general_config = source.load(GeneralConfig)\n   assert general_config == GeneralConfig(log_level="DEBUG", show_warnings=True)\n\n   foobar_config = source.load(FoobarConfig, \'foobar\')\n   assert foobar_config.some == "thing"\n\n\n\na structlog\n-----------\n\nI want to have a nice and readable `structlog`_ in my terminal and a json log in\nproduction.\n\n.. code-block:: python\n\n   import sys\n\n   from buvar import log\n\n   log.setup_logging(sys.stdout.isatty(), general_config.log_level)\n\n\n.. _Pyramid: https://github.com/Pylons/pyramid\n.. _structlog: https://www.structlog.org/en/stable/\n',
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
