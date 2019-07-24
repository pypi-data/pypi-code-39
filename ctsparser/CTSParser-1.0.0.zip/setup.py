from distutils.core import setup

setup(
    name = 'CTSParser',
    packages = ['CTSParser'],
    version = '1.0.0',
    description = 'The tool is for parsing CTS report.',
    author = 'Dramon Studio',
    author_email = 'yang1365g@gmail.com',
    url = 'https://github.com/DramonStudio/CTSParser',
    download_url = 'https://github.com/DramonStudio/CTSParser/',
    keywords = ['CTS','Google','Parser'],
    install_requires=[          
          'httpimport',
      ]
)