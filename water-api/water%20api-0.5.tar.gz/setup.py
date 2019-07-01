from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='water api',
      version='0.5',
      description='A general container of apis out of Naver, Kakao',
      url='https://github.com/harry81/naver_api',
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
