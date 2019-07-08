# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['arg_dispatch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'arg-dispatch',
    'version': '0.1.3',
    'description': 'function can be dispatched by its arguments',
    'long_description': "# arg_dispatch\nfunction can be dispatched by its arguments\n\n## Example\n```python\nfrom arg_dispatch import dispatch\n\n\n# Functions\n@dispatch\ndef demo(a, b):\n    return 'hello'\n    \n@dispatch\ndef demo(c):\n    return 'world'\n    \n\ndemo(a=1, b=2)  # return 'hello'\ndemo(c=3)       # return 'world'\n\n# try to call a function which has not been registed\ndemo(d=4)       # raise `FunctionNotRegist`\n\n# Methods\nclass Demo(object):\n    @dispatch\n    def demo(self, a, b):\n        return 'hello'\n        \n    @dispatch\n    def demo(self, c):\n        return 'world'\n        \ninstance = Demo()\ninstance.demo(a=1, b=2)  # return 'hello'\ninstance.demo(c=3)       # return 'world'\n\n# try to call a method which has not been registed\ninstance.demo(d=4)       # raise `FunctionNotRegist`\n```\n\n## Notice💣\n**positional arguments must be required**\n```python\ndemo(1, 2)          # Boom!💣, raise `ArgumentError`\ninstance.demo(1, 2) # Boom!💣, raise `ArgumentError`\n```\n\n**default value is also not supported**\n```python\n@dispatch\ndef demo(a, b=1):            # Boom!💣, raise `ExistDefaultValue`\n    return 'hello'\n    \nclass Demo(object):\n    @dispatch\n    def demo(self, a, b=1):  # Boom!💣, raise `ExistDefaultValue`\n        return 'hello'\n```\n",
    'author': 'zen-xu',
    'author_email': 'zen-xu@outlook.com',
    'url': 'https://github.com/zen-xu/arg_dispatch',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
