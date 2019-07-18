# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['httprunner']

package_data = \
{'': ['*'], 'httprunner': ['templates/*']}

install_requires = \
['colorama>=0.4.1,<0.5.0',
 'colorlog>=4.0,<5.0',
 'filetype>=1.0,<2.0',
 'har2case>=0.3.1,<0.4.0',
 'jinja2>=2.10,<3.0',
 'pyyaml>=5.1,<6.0',
 'requests-toolbelt>=0.8.0,<0.9.0',
 'requests>=2.14,<3.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['future>=0.17.1,<0.18.0']}

entry_points = \
{'console_scripts': ['ate = httprunner.cli:main_hrun',
                     'hrun = httprunner.cli:main_hrun',
                     'httprunner = httprunner.cli:main_hrun',
                     'locusts = httprunner.cli:main_locust']}

setup_kwargs = {
    'name': 'httprunner',
    'version': '2.2.4',
    'description': 'One-stop solution for HTTP(S) testing.',
    'long_description': "# HttpRunner\n\n[![LICENSE](https://img.shields.io/github/license/HttpRunner/HttpRunner.svg)](https://github.com/HttpRunner/HttpRunner/blob/master/LICENSE) [![travis-ci](https://travis-ci.org/HttpRunner/HttpRunner.svg?branch=master)](https://travis-ci.org/HttpRunner/HttpRunner) [![coveralls](https://coveralls.io/repos/github/HttpRunner/HttpRunner/badge.svg?branch=master)](https://coveralls.io/github/HttpRunner/HttpRunner?branch=master) [![pypi version](https://img.shields.io/pypi/v/HttpRunner.svg)](https://pypi.python.org/pypi/HttpRunner) [![pyversions](https://img.shields.io/pypi/pyversions/HttpRunner.svg)](https://pypi.python.org/pypi/HttpRunner)\n\nHttpRunner is an HTTP(S) protocol-oriented universal testing framework. Write testing scripts in `YAML/JSON` once, you can then achieve automated testing, performance testing, online monitoring, continuous integration and other testing needs.\n\nFormerly known as `ApiTestEngine`.\n\n## Design Philosophy\n\n- Take full reuse of Python's existing powerful libraries: [`Requests`][Requests], [`unittest`][unittest] and [`Locust`][Locust].\n- Convention over configuration.\n- Pursuit of high rewards, write once and achieve a variety of testing needs\n\n## Key Features\n\n- Inherit all powerful features of [`Requests`][Requests], just have fun to handle HTTP(S) in human way.\n- Define testcases in YAML or JSON format in concise and elegant manner.\n- Record and generate testcases with [`HAR`][HAR] support. see [`har2case`][har2case].\n- Supports `function`/`variable`/`extract`/`validate` mechanisms to create full test scenarios.\n- Supports perfect hook mechanism.\n- With `debugtalk.py` plugin, module functions can be auto-discovered in recursive upward directories.\n- Testcases can be run in diverse ways, with single testcase, multiple testcases, or entire project folder.\n- Test report is concise and clear, with detailed log records.\n- With reuse of [`Locust`][Locust], you can run performance test without extra work.\n- CLI command supported, perfect combination with `CI/CD`.\n\n## Documentation\n\nHttpRunner is rich documented.\n\n- [`User documentation in English (outdated)`][user-docs-en]\n- [`中文用户使用手册`][user-docs-zh]\n- [`开发历程记录博客`][development-blogs]\n\n## How to Contribute\n\n1. Check for [open issues](https://github.com/HttpRunner/HttpRunner/issues) or [open a fresh issue](https://github.com/HttpRunner/HttpRunner/issues/new/choose) to start a discussion around a feature idea or a bug.\n2. Fork [the repository](https://github.com/httprunner/httprunner) on GitHub to start making your changes to the **master** branch (or branch off of it). You also need to comply with the [development rules](docs/dev-rules.md).\n3. Write a test which shows that the bug was fixed or that the feature works as expected.\n4. Send a pull request, you will then become a [contributor](https://github.com/HttpRunner/HttpRunner/graphs/contributors) after it gets merged and published.\n\n## Subscribe\n\n关注 HttpRunner 的微信公众号，第一时间获得最新资讯。\n\n![][qrcode_for_httprunner]\n\n[Requests]: http://docs.python-requests.org/en/master/\n[unittest]: https://docs.python.org/3/library/unittest.html\n[Locust]: http://locust.io/\n[PyUnitReport]: https://github.com/HttpRunner/PyUnitReport\n[Jenkins]: https://jenkins.io/index.html\n[har2case]: https://github.com/HttpRunner/har2case\n[user-docs-en]: http://httprunner.org/\n[user-docs-zh]: http://cn.httprunner.org/\n[development-blogs]: http://debugtalk.com/tags/HttpRunner/\n[HAR]: http://httparchive.org/\n[Swagger]: https://swagger.io/\n[Postman Collection Format]: http://blog.getpostman.com/2015/06/05/travelogue-of-postman-collection-format-v2/\n[qrcode_for_httprunner]: https://raw.githubusercontent.com/HttpRunner/HttpRunner/master/docs/images/qrcode_for_httprunner.jpg\n",
    'author': 'debugtalk',
    'author_email': 'debugtalk@gmail.com',
    'url': 'https://github.com/HttpRunner/HttpRunner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
