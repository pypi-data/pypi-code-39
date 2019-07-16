from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'django_xfields',
  packages=find_packages(exclude=("tests",)),
  version = '0.2',
  license = 'MIT License',
  description = 'Extra fields for Django framework',
  author = 'leviplj',
  author_email = 'leviplj@gmail.com',
  url = 'https://github.com/leviplj/django_xfields',
  download_url = 'https://github.com/leviplj/django_xfields/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['django', 'fields', 'extra'],
  install_requires=[
    'django',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)