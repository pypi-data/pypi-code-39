from distutils.core import setup
setup(
  name = 'taskmonk-sdk',         # How you named your package folder (MyLib)
  packages = ['taskmonk-sdk'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='apache-2.0',        # Chose a license from here: 
  description = 'SDK for accessing TaskMonk functionality',   # Give a short description about your library
  author = 'Taskmonk',                   # Type in your name
  author_email = 'info@taskmonk.com',      # Type in your E-Mail
  url = 'https://github.com/taskmonk/taskmonk-sdk',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/taskmonk/taskmonk-sdk/archive/v_0.1.tar.gz',    # I explain this later on
  keywords = ['TaskMonk', 'SDK'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
