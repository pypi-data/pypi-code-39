from distutils.core import setup
setup(
  name = 'dfw511',
  packages = ['dfw511'],
  version = '0.0.4',
  license='MIT',
  description = 'Python library to retrieve information and convert to json from 511dfw.org',
  author = 'Ian Duncan',
  author_email = 'duncan.ian.t@gmail.com',
  url = 'https://github.com/IanDuncanT/dfw511',
  download_url = 'https://github.com/IanDuncanT/dfw511/archive/v0.0.4.tar.gz',
  keywords = ['Traffic', 'DFW', '511', 'Traffic Information', '511dfw', 'DFW 511'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      #"3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
