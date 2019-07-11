from distutils.core import setup

setup(
  name = 'PotatLib',         # How you named your package folder (MyLib)
  packages = ['PotatLib'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Library to add Support for Plugin Developers at Defuse Solutions',   # Give a short description about your library
  author = 'Devon Rickman',                   # Type in your name
  author_email = 'drickman180@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/NightPotato/PotatLib',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/NightPotato/PotatLib/archive/0.2.tar.gz',    # I explain this later on
  keywords = ['Plugin Development', 'Defuse Discord Bot', 'PotatLib'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
  ],
)