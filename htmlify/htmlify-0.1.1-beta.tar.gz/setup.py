from distutils.core import setup

# read the contents of your README file
# stolen shamelessly from docs
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'htmlify',
  packages = ['htmlify'],
  version = '0.1.1-beta',
  license='MIT',
  description = 'An ultra-basic, human-friendly templating system for doing CGI with Python for less 😕 and more 🎉',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Theo Court',
  author_email = 'theo.court@pm.me',
  url = 'https://github.com/iDoObject/htmlify',
  download_url = 'https://github.com/iDoObject/htmlify/archive/v0.1.1-beta.tar.gz',
  keywords = ['CGI', 'python3', 'HTML', 'templates', 'templating'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)