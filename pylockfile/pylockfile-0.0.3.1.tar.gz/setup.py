from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='pylockfile',
      version='0.0.3.1',
      packages=find_packages(),
      author='Kusakin Anton @iiiparadoxxxiii',
      author_email='iiiparadoxxxiii@gmail.com',
      url='https://github.com/iiiparadoxxxiii/lockfile',
      description="Создание файла блокировки, для предотвращения выполнения нескольких копий скрипта",
      long_description=long_description,
      long_description_content_type="text/markdown",
      )
