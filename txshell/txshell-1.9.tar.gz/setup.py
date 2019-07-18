from distutils.core import setup
setup(
  name = 'txshell',
  packages = ['Tssh'],
  version = '1.9',
  license='MIT',
  description = 'hacking shell for termux . by 22bit',
  author = '22bit',
  author_email = '22bit@protonmail.com',
  url = 'https://github.com/22bit/tshx.git',
  download_url = 'https://github.com/22bit/tshx.git',
  keywords = ['tsh', 'shell', 'thundershell'],
  install_requires=[
          'future',
          'bs4',
          'requests',
          'colorama',
          'wget==3.2',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',    'License :: OSI Approved :: MIT License',   # Again, pick a license    'Programming Language :: Python :: 3',    
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)