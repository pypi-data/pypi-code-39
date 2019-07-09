from distutils.core import setup

setup(name='html2csv',
      version='1.0.0',
      description='Automatically download almost any spreadsheet from any website.',
      long_description='A Python script designed to Automatically download any almost spreadsheet from any website.',
      author='sl4v',
      author_email='iamsl4v@protonmail.com',
      url='https://github.com/sl4vkek/html2csv',
      install_requires = ['BeautifulSoup4'],
      license="WTFPL",
      entry_points={
            'console_scripts':[
                  'html2csv = html2csv.__main__:main'
            ]
      }
)
