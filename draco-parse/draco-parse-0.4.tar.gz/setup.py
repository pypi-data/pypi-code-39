from setuptools import setup, find_packages

setup(name='draco-parse',
      version='0.4',
      url='https://github.com/roberto/parse',
      license='MIT',
      author='Roberto',
      author_email='roberto.gonzales@gmail.com',
      description='Parse and test purpose',
      packages=find_packages(exclude=['ejemplo']),
      long_description=open('README.md').read(),
      install_requires=['validators','bs4'],
      zip_safe=False)