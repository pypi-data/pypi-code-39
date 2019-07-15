from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'taskmonk-sdk',         # How you named your package folder (MyLib)
  packages = ['taskmonk', 'taskmonk.utils'],   # Chose the same as "name"
  version = '0.8',      # Start with a small number and increase it with every change you make
  license='apache-2.0',        # Chose a license from here: 
  description = 'SDK for accessing TaskMonk functionality',   # Give a short description about your library
  author = 'Taskmonk',                   # Type in your name
  author_email = 'info@taskmonk.com',      # Type in your E-Mail
  url = 'https://github.com/taskmonk/taskmonk-sdk-python',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/taskmonk/taskmonk-sdk-python/archive/v_0.8.tar.gz',    
  keywords = ['TaskMonk', 'SDK'],   # Keywords that define your package best
  install_requires=[            
  	'requests'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
