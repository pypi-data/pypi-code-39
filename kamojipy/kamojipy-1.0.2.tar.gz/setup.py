from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='kamojipy',
      version='1.0.2',
      description='Add kamoji to your python file github.com/SafyreLyons/kamojipy',
      url='https://github.com/SafyreLyons/kamojipy',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Safyre Lyons',
      author_email='lyons.safyre@gmail.com',
      license='MIT',
      py_modules=['kamojipy'],
      package_dir={'': 'src'},
      zip_safe=False)