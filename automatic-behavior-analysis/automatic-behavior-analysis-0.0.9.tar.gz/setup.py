# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['analitics',
 'client',
 'client.plugins',
 'client2',
 'server',
 'tools',
 'tools.labelImg',
 'tools.labelImg.libs',
 'util',
 'util.digNetwork']

package_data = \
{'': ['*'],
 'client': ['dialogs/*', 'widgets/*'],
 'client2': ['tools/*'],
 'server': ['config/config.1.json',
            'config/config.1.json',
            'config/config.1.json',
            'config/config.1.json',
            'config/config.2.json',
            'config/config.2.json',
            'config/config.2.json',
            'config/config.2.json',
            'config/config.3.json',
            'config/config.3.json',
            'config/config.3.json',
            'config/config.3.json',
            'config/config.example.json',
            'config/config.example.json',
            'config/config.example.json',
            'config/config.example.json'],
 'tools.labelImg': ['build-tools/*',
                    'demo/*',
                    'requirements/*',
                    'resources/icons/*',
                    'resources/strings/*',
                    'tests/*']}

install_requires = \
['PyQt5', 'appdirs', 'opencv-python']

entry_points = \
{'console_scripts': ['aba-client = client2:run.main']}

setup_kwargs = {
    'name': 'automatic-behavior-analysis',
    'version': '0.0.9',
    'description': 'Program complex for automated behavior analysis',
    'long_description': '# AutomaticBehaviorAnalysis\n\n## Установка\n### pip\nКлиент (в режиме работы с кеша)\nДля работы с кеша нужно разместить видео и файл кэша в одну папку\n\nУстановка пакета:\n\n`pip install --user automatic-behavior-analysis`\n\nОбновление пакета:\n\n`pip install --upgrade --user automatic-behavior-analysis`\n\nЗапуск клиента:\n\n`aba-client`\n\nПеред первым запуском после установки надо перейти в папку\n`~/.local/lib/python3.7/site-packages/client2/`\n И создать копию файла config.1.json с именем config.json\n\n## Требования\n\n* Python 3\n* TensorFlow\n* [Tensorflow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)\n* Keras\n* numpy\n* PIL\n* tkinter\n* appdirs\n* openCV\n* websocket\n\n### Client2\n\n* Python 3\n* openCV\n* appdirs\n\n## Сборка контейнера с сервером\n\n### Контейнер для разработки\n\nВ контейнере для разработки отсутствуют файлы и модели с целью минификации образа и повышения удобства работы.\n\nКонтейнер собирается следующей командой:\n\n```bash\n# Для контейнера с поддержкой GPU\ndocker build -t registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-gpu .\n# Для контейнера с поддержкой только CPU\ndocker build  -f Dockerfile.dev.cpu -t registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu .\n```\n\nДля работы нет необходимости пересобирать контейнер и можно забрать собранный с репозитория с помощью следующих команд:\n\n```bash\ndocker login registry.gitlab.com\n# Для запуска контейнера с поддержкой GPU\ndocker run --runtime=nvidia -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-gpu:latest\n\n# Для запуска контейнера с поддержкой CPU\ndocker run -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu:latest\n```\n\nДля CPU-only:\n\n```bash\ndocker login registry.gitlab.com\ndocker run -it -v <workspace>:/home/user/ -p 1217:1217 registry.gitlab.com/digiratory/automatic-behavior-analysis/dev-cpu:latest\n```\n\nЕсли на машине отсутствует gpu, то ключ `--runtime=nvidia` указывать не надо.\n\nВНИМАНИЕ! Контейнер для разработки не включает в свой состав исходный код, модели и прочее.\n\n## Запуск приложений\n\nПорядок запуска:\n\n1. Серверная часть\n2. Клиентская часть\n\nПорядок выключения:\n\n1. Клиентская часть\n2. Серверная часть\n\n### Сервер\n\nДля запуска серверной части необходимо выполнить ./server.py\n\n```bash\npython3 ./server.py\n```\n\nАргументы команды:\n[ip= ] — Ip адрес для прослушки (По умолчанию 172.0.0.1 )\n[port= ] — Порт сервера (По умолчанию 1217)\n\n### Клиентская часть (GUI)\n\nДля запуска серверной части необходимо выполнить ./client_gui.py\n\n```bash\npython3 ./client_gui.py\n```\n\nАргументы команды:\n[ip= ] — Ip адрес сервера (По умолчанию 172.0.0.1 )\n[port= ] — Порт сервера (По умолчанию 1217)\n',
    'author': 'Aleksandr Sinitca',
    'author_email': 'siniza.s.94@gmail.com',
    'url': 'https://gitlab.com/digiratory/automatic-behavior-analysis/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
