from distutils.core import setup
setup(
  name = 'lushdwlib',         # How you named your package folder (MyLib)
  packages = ['lushdwlib'],   # Chose the same as "name"
  version = '1.0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python Libraries for pullers',   # Give a short description about your library
  author = 'Denis Sineiko',                   # Type in your name
  author_email = 'denis.sineiko@lush.co.uk',      # Type in your E-Mail
  url = 'https://gitlab.com/LUSHDigital/data-warehouse/bqload_scripts',   # Provide either the link to your github or to your website
  download_url = 'http://zonec.net/lushdwlib.tar',    # I explain this later on
  keywords = ['PYTHON', 'LUSH', 'PULLERS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'google-cloud-bigquery',
          'slackclient',
          'environs',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
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


