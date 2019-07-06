from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name='sptemp',
      version='1.1.0',
      description='package for spatio-temporal vector data processing and analysis.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Daniel Baumann',
      author_email='baumann-dan@outlook.com',
      url = 'https://github.com/BaumannDaniel/sptemp',
      packages=find_packages(),
      package_dir={'sptemp':'sptemp'},
      classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
      zip_safe=False)