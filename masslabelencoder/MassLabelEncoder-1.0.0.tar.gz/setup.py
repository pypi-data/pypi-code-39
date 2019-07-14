from distutils.core import setup
setup(
  name = 'MassLabelEncoder',         # How you named your package folder (MyLib)
  packages = ['MassLabelEncoder'],   # Chose the same as "name"
  version = '1.0.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Custom label encoder for mass datasets. Creates custom aggregate dictionary containing all scikit-learn labelencoding models for columns in pandas dataframe.',   # Give a short description about your library
  author = 'JCIB ForensX',                   # Type in your name
  author_email = 'aniketpant@jefcoed.com',      # Type in your E-Mail
  url = 'https://github.com/AniketPant02/mass_labelencoder',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/AniketPant02/mass_labelencoder/archive/v1.0.tar.gz',    # I explain this later on
  keywords = ['LabelEncoder'],   # Keywords that define your package best
  install_requires=[
          'pandas', 'scikit-learn', 'numpy'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)