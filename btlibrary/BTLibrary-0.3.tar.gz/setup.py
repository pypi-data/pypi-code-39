from distutils.core import setup
setup(
  name = 'BTLibrary',
  packages = ['BTLibrary'],   
  version = '0.3',      
  license='MIT',       
  description = 'This package is used to provide various utilities for project support.',   
  author = 'David Sinex',                   
  author_email = 'dave.sinex@btgeophysics.com',    
  url = 'http://www.btgeophysics.com',  
  download_url = 'https://github.com/humberto77/BTUtilities/archive/R0_3.tar.gz',    
  keywords = ['Utilities', 'BTG'],   
  install_requires=[           
          'jsonpickle',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
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