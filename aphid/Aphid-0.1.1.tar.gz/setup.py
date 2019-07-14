import setuptools


with open(r'C:\Users\Owner\Documents\Aphid\README.md', 'r') as file:
      long = file.read()
setuptools.setup(name='Aphid',
      version='0.1.1',
      description='A toolkit for working with nested data types',
      long_description=long,
      long_description_content_type="text/markdown",
      author='Robert Kearns',
      author_email='rxk0914@hotmail.com',
      url='https://github.com/robertkearns/Aphid',
      packages=['Aphid']
      )
