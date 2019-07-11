from setuptools import setup, find_packages
setup(
name='quickim',
version = "0.2.1",
description = "QuickIM client application",
author = "Artem Naumov",
author_email = "simperu@yandex.ru",
long_description="Client for QuickIM messenger",
include_package_data=True,
python_requires='>=3.5',
install_requires=['PyQt5>=5.9','SQLAlchemy>=1.1.15'],
url = "https://github.com/Simper007/quickIM",
packages = ["src","src.logs","src.logs.config"]
)