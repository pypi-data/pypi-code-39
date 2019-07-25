from distutils.core import setup
setup(
  name = 'htmlify',
  packages = ['htmlify'],
  version = '0.1-beta',
  license='MIT',
  description = 'An ultra-basic, human-friendly templating system for doing CGI with Python for less 😕 and more 🎉',
  author = 'Theo Court',
  author_email = 'theo.court@pm.me',
  url = 'https://github.com/iDoObject/htmlify',
  download_url = 'https://github.com/iDoObject/htmlify/archive/v0.1-beta.tar.gz',
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