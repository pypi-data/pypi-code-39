# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['blogger_cli',
 'blogger_cli.blog_manager',
 'blogger_cli.cli_utils',
 'blogger_cli.commands',
 'blogger_cli.commands.convert_utils',
 'blogger_cli.commands.export_utils',
 'blogger_cli.converter',
 'blogger_cli.resources',
 'blogger_cli.tests']

package_data = \
{'': ['*'],
 'blogger_cli': ['docs/*'],
 'blogger_cli.resources': ['blog_layout/*',
                           'blog_layout/_blogger_templates/*',
                           'blog_layout/assets/css/*',
                           'blog_layout/blog/*'],
 'blogger_cli.tests': ['tests_resources/*',
                       'tests_resources/_blogger_templates/*',
                       'tests_resources/index/*',
                       'tests_resources/results/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=7.0,<8.0',
 'markdown>=3.1,<4.0',
 'nbconvert>=5.5,<6.0']

entry_points = \
{'console_scripts': ['blogger = blogger_cli.cli:cli']}

setup_kwargs = {
    'name': 'blogger-cli',
    'version': '1.0.0a3',
    'description': 'Blogger cli is a CLI tool to convert ipynb, md, txt file to responsive html files.',
    'long_description': "# Blogger-cli\nA custom cli tool to process jupyter notebooks, markdown files and html files. Write your blog in markdown or jupyter notebooks and then transform into blog post with mathjax, code support, google analytics, navigation, disqus support.\n\n\n## Why?\nIt is easy to get your hands on, works flawlessly and won't get bulky and slow overtime.\nBlogger-cli has simple conversion system that is fast as well extremely customizable. \n\n\n## Features\n* Robust conversion of ipynb notebooks with great support for mobile devices as well.\n* Built in support for disqus, google analytics, navigation bar, mathjax and code highlighting.\n* Blog management: updating index, parsing out images, managing topics and metadata. \n* Write and post blogs from android or any micro device. All that is required is command line with python and pip.\n* Built in design, blog_templates for rapidly setting up your blog from scratch.\n* Fully customizable with support for custom themes and templates\n* Also support conversion of other file formats like markdown. You can also implement your own.\n\n\n## 💻 Installation\n\n### Recommended Method\n```\n$ curl -sSL https://raw.githubusercontent.com/hemanta212/blogger-cli/master/get_blogger.py | python\n```\nSince blogger has alot of dependecies (nbconvert, jupyter), this custom installer will install in a virtualenv and add it to your path for global access!.\n\n### Using pip\n```\npip install blogger-cli\n```\n\nIf you mainly use jupyter notebook, then you already have all dependecies although it is recommende to use virutalenv.\n\n\n## 🚀 Getting Started\nMake a website repository and clone it to your computer. Now register your blogname with blogger\n```$ blogger addblog <blogname>```\nand setup necessary configs. Now, If you have new site or empty site. You can get blogger default design and boiler plate.\n```\n$ blogger export blog_layout -b <blogname>\n```\nNow, all assets will be moved to the blog_dir you specified in the blog config during setup.\n```\n$ blogger serve <blogname>\n```\nOpen the url http://localhost:8000/ in your browser to view your blog!!\n\n## 📖 Documentation\n- [Installation, update, uninstall methods](blogger_cli/docs/installation.md)\n- [Managing blogs and configurations](blogger_cli/docs/blog_management.md)\n- [Conversion of files and folders](blogger_cli/docs/conversion.md)\n- [Serving blog locally](blogger_cli/docs/serving_blog_locally.md)\n- [Using export command](blogger_cli/docs/export.md)\n- [Customizing templates and design](blogger_cli/docs/customizing.md)\n- [Writing blog's metadata](blogger_cli/docs/meta.md)\n- [Recommended workflow for blogger-cli](blogger_cli/docs/workflow.md)\n\n## Author\n\n👤 **Hemanta Sharma**\n- Github: [@hemanta212](https://github.com/hemanta212)\n\n## Special Thanks\n\n👤 **Nipun Batra** : Inspiration for core conversion mechanism and design resources.\n- Github: [@nipunbatra](https://github.com/nipunbatra)\n- His article on ipynb conversion: [@nipunbatra.github.io](https://nipunbatra.github.io/blog/2017/Jupyter-powered-blog.html)\n\n## Show your support\n\nPlease ⭐️ this repository if this project helped you!\n\n## 📝 License\nCopyright © 2019 [Hemanta Sharma](https://github.com/kefranabg).<br />\nThis project is [MIT](LICENSE) licensed.\n---\n",
    'author': 'hemanta212',
    'author_email': 'sharmahemanta.212@gmail.com',
    'url': 'https://github.com/hemanta212/blogger-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
