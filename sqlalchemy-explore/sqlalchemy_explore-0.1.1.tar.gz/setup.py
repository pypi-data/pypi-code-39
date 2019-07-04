from distutils.core import setup
setup(
  name = 'sqlalchemy_explore',         # How you named your package folder (MyLib)
  packages = ['sqlalchemy_explore'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Utilities for working with pre-existing databases using SQLAlchemy',   # Give a short description about your library
  author = 'Aviad Rozenhek',                   # Type in your name
  author_email = 'aviadr1@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/aviadr1/sqlalchemy-explore',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/aviadr1/sqlalchemy-explore/archive/v0.1.tar.gz',    # I explain this later on
  keywords = ['SQLAlchemy', 'reflect', 'explore', 'dump', 'automap'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'sqlalchemy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
  ],
)

"""
how to distribute:
follow https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

python setup.py sdist
pip install twine
twine upload dist/*
pip install sqlalchemy_explore
"""