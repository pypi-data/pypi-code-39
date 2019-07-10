from setuptools import setup, find_packages

setup(name="Another_One_Messenger_Server",
      version="0.9",
      description="Messenger_server",
      author="Mihail Pendyurin",
      author_email="mihail.pendyurin@rt.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
