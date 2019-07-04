# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['slack_channeler']

package_data = \
{'': ['*']}

install_requires = \
['channels>=2.2,<3.0', 'click>=7.0,<8.0', 'slackclient>=2.0,<3.0']

entry_points = \
{'console_scripts': ['slack_channeler = slack_channeler.cli:main']}

setup_kwargs = {
    'name': 'slack-channeler',
    'version': '0.0.1.dev0',
    'description': 'Power a Slack bot with Django Channels v2',
    'long_description': '# slack-channeler\nPower a Slack bot with Django Channels v2\n\n\n# Installation\n```bash\npip install slack-channeler\n```\n\n\n# Usage\nslack-channeler relies on the channel layer. First, ensure it\'s setup. [channels-redis](https://github.com/django/channels_redis) is recommended.\n```python\n# settings.py\n\nCHANNEL_LAYERS = {\n    \'default\': {\n        \'BACKEND\': \'channels_redis.core.RedisChannelLayer\',\n        \'CONFIG\': {\n            "hosts": [(\'localhost\', 6379)],\n        },\n    },\n}\n```\n\nCreate a consumer to handle Slack events\n```python\n# consumers.py\n\nfrom channels.consumer import AsyncConsumer, get_handler_name\n\nclass SlackConsumer(AsyncConsumer):\n    async def dispatch(self, message):\n        handler = getattr(self, get_handler_name(message), None)\n        if handler:\n            await handler(**message[\'data\'])\n\n    async def slack_message(self, channel, text, **kwargs):\n        # Simply echo back message\n        await self.channel_layer.send(\'slack\', {\n            \'type\': \'message\',\n            \'channel\': channel,\n            \'text\': text,\n        })\n```\n\nRoute Slack events to the consumer\n```python\n# routing.py\n\nfrom channels.routing import ProtocolTypeRouter, ChannelNameRouter\n\nfrom .consumers import SlackConsumer\n\napplication = ProtocolTypeRouter({\n    \'channel\': ChannelNameRouter({\n        \'slack\': SlackConsumer,\n    }),\n})\n```\n\nStart a Channels worker to handle Slack events from the channel layer\n```bash\npython manage.py runworker slack\n```\n\nLastly, run slack-channeler\n```bash\nSLACK_CHANNELER_TOKEN=xoxb-12345678900-098765432100-DeadBeefFeed90iIJjYsf3ay slack_channeler\n```\n\n\n# Building package\nCurrently, poetry does not support dynamic generation of version files, nor custom hooks to do so. To keep `pyproject.toml` the source of authority for version numbers, a custom `build.py` script is used to dynamically generate `version.py`.\n\nTo build slack-channeler, run `python build.py`. This has the same semantics as `poetry build`.\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
