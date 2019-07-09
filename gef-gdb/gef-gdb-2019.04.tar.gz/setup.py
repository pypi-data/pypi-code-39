from distutils.core import setup
setup(
  name = 'gef-gdb',         # How you named your package folder (MyLib)
  packages = ['gef-gdb'],   # Chose the same as "name"
  version = '2019.04',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: 
  description = 'I am not the owner of this project, see --> https://github.com/hugsy/gef',   # Give a short description about your library
  author = '@_hugsy_',                   # Type in your name
  author_email = 'UNKNOWN@UNKNOWN.UNKNOWN',      # Type in your E-Mail
  url = 'https://github.com/hugsy/gef',   # Provide either the link to your github or to your website
  keywords = ['gef', 'gdb'],   # Keywords that define your package best
  install_requires=[           
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support,
    'Programming Language :: Python :: 2',      #Specify which pyhton versions that you want to support
  ],
)