from setuptools import setup

with open("README.md", "r") as fh:
    long_description = 'hi'

setup(name='krawler-api',
      version='0.8',
      description='A general container of apis out of Naver, Kakao',
      url='https://github.com/harry81/krawler',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Hyunmin Choi',
      author_email='pointer81@gmail.com',
      license='MIT',
      packages=['water'],
      install_requires=[
          'bs4', 'requests'
      ],
      zip_safe=False)
