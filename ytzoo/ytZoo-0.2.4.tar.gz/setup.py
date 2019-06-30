from distutils.core import setup
from ytZoo import __version__

setup(
  name = 'ytZoo',         # How you named your package folder (MyLib)
  packages = ['ytZoo'],   # Chose the same as "name"
  version=__version__,  # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Day-to-day programming utilities.',   # Give a short description about your library
  author = 'Alan H Yue',                   # Type in your name
  author_email = 'alanhyue@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/alanhyue/ytZoo',   # Provide either the link to your github or to your website
  keywords = ['ytZoo'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas'
      ],
  package_data={'ytZoo': ['datatools/pandas_flavor/*.py', 'datatools/*.py', 'ML/*.py']},
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
