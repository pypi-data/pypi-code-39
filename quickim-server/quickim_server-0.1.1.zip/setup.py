from setuptools import setup
setup(
name='quickim_server',
version = "0.1.1",
description = "QuickIM server application",
author = "Artem Naumov",
author_email = "simperu@yandex.ru",
url = "https://github.com/Simper007/quickIM",
long_description="Server for QuickIM messenger",
include_package_data=True,
python_requires='>=3.5',
install_requires=['PyQt5>=5.9','SQLAlchemy>=1.1.15'],
packages = ["src","src.logs","src.logs.config"]
)