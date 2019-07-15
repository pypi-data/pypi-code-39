# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['forkwork']

package_data = \
{'': ['*']}

install_requires = \
['cachecontrol>=0.12.5,<0.13.0',
 'click>=7.0,<8.0',
 'github3.py>=1.3,<2.0',
 'halo>=0.0.26,<0.0.27',
 'lockfile>=0.12.2,<0.13.0',
 'pendulum>=2.0,<3.0',
 'tabulate>=0.8.3,<0.9.0']

entry_points = \
{'console_scripts': ['forkwork = forkwork.forkwork:cli']}

setup_kwargs = {
    'name': 'forkwork',
    'version': '0.0.3',
    'description': 'Find maintained forks of your favorite repositories',
    'long_description': '# Forkwork\n\nThis might help to find maintained alternatives of an abandoned repo.\n\nInspired by [forked](https://github.com/ys/forked)   \n\n\n## Requirements\n* Python 3.5 and up\n\n## Installation\nfrom PyPI\n```\n$ pip install forkwork\n```\n\nfrom git repository\n```\n$ pip install git+https://github.com/andriyor/forkwork.git\n```\n\nfrom source\n```\n$ git clone https://github.com/andriyor/forkwork.git\n$ cd forkwork\n$ python setup.py install\n```\n\n## Usage\n\nTo prevent rale limit being exceeded for unauthentIcated requests, forkwork needs an access token.\nFor public repositories, [create a token](https://github.com/settings/tokens/new?scopes=public_repo&description=forkwork) \nwith the public_repo permission.\n\nYou can use token as environment variable ``FORKWORK_TOKEN`` at ``~/.bashrc`` or ``~/.zshrc`` \n\nexport FORKWORK_TOKEN="****************************************"\n\nor pass token as option --token\n\n```\n$ forkwork --help\nUsage: forkwork [OPTIONS] URL COMMAND [ARGS]...\n\nOptions:\n  --token TEXT\n  --help        Show this message and exit.\n\nCommands:\n  fnm\n  top\n```\ntop command option\n```\n$ forkwork https://github.com/voronind/vk top --help                \nUsage: forkwork top [OPTIONS]\n\nOptions:\n  --n INTEGER           Numbers of rows\n  -S, --star            Sort by stargazers count\n  -F, --forks           Sort by forks count\n  -I, --open_issues     Sort by open issues count\n  -W, --watchers_count  Sort by watchers count\n  -D, --updated_at      Sort by updated at\n  -P, --pushed_at       Sort by pushed at\n  -C, --commits         Sort by number of commits\n  -B, --branches        Sort by number of branches\n  --help                Show this message and exit.\n```\n\n### Example usage\nfind top repo\n```\n➜ poetry run forkwork https://github.com/mattdiamond/Recorderjs top -F --n=5\n+-----------------------------------------------+---------+---------+---------------+------------+-------------------+--------------+\n| URL                                           |   Stars |   Forks |   Open Issues |   Watchers | Last update       | Pushed At    |\n+===============================================+=========+=========+===============+============+===================+==============+\n| https://github.com/chris-rudmin/opus-recorder |     594 |     107 |             6 |        594 | a few seconds ago | 2 months ago |\n+-----------------------------------------------+---------+---------+---------------+------------+-------------------+--------------+\n| https://github.com/remusnegrota/Recorderjs    |      45 |      15 |             0 |         45 | 2 months ago      | 5 years ago  |\n+-----------------------------------------------+---------+---------+---------------+------------+-------------------+--------------+\n| https://github.com/jergason/Recorderjs        |      11 |      12 |             3 |         11 | 2 months ago      | 2 years ago  |\n+-----------------------------------------------+---------+---------+---------------+------------+-------------------+--------------+\n| https://github.com/rokgregoric/html5record    |      41 |       7 |             0 |         41 | 8 months ago      | 7 years ago  |\n+-----------------------------------------------+---------+---------+---------------+------------+-------------------+--------------+\n| https://github.com/somnumDotIo/Recorderjs     |       0 |       2 |             0 |          0 | 3 years ago       | 3 years ago  |\n+-----------------------------------------------+---------+---------+---------------+------------+-------------------+--------------+\n```\n\nfind commit that don\'t merged and not pushed to a pull request\n```\n$ forkwork https://github.com/dimka665/vk fnm\n\n Detrous https://github.com/Detrous/vk\n1 add: proxy https://github.com/Detrous/vk/commit/87718dab306484716470fb5b1e13d7b676b1bd7b\n\n andriyor https://github.com/andriyor/vk\n1 add support proxies\ndefault\xa0 API version https://github.com/andriyor/vk/commit/8523ed081ea8370d7a9b6664bd8d0882ec512480\n```\n\n```\n$ forkwork https://github.com/MongoEngine/eve-mongoengine fnm\n\n Aldream https://github.com/Aldream/eve-mongoengine\n1 <attempt> Update requirements https://github.com/Aldream/eve-mongoengine/commit/3f2617b2cf978adab9296d6be9d293243d05c76e\n\n wdtbrno https://github.com/wdtbrno/eve-mongoengine\n1 Remove autocreating where based on headers If-Modified-Since\n\nPython-eve since 0.5 disabled If-Modified-Since on resource endpoints\nSame functionality is available with\na ?where={"_udpated": {"$gt": "<RFC1123 date>"}} request. https://github.com/wdtbrno/eve-mongoengine/commit/9cb2ac3abbc210f37daff98bf5c6a3e638aeeb84\n```\n\n\n## Development setup\nInstall [Pipenv](https://docs.pipenv.org/)   \n```\n$ pipenv install --dev -e .\n```\nor [Poetry](https://poetry.eustace.io/docs/)   \n```\n$ poetry install\n```\nrun tests\n```\n$ poetry run pytest\n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Andriy Orehov',
    'author_email': 'andriyorehov@gmail.com',
    'url': 'https://github.com/github-tooling/forkwork',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
