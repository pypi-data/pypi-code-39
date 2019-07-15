from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='hewwwo',
      version='1.0.0',
      description='hewwo wowwd uwu',
      url='https://github.com/SafyreLyons/hewwwo',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Safyre Lyons',
      author_email='lyons.safyre@gmail.com',
      license='MIT',
      py_modules=['hewwwo'],
      package_dir={'': 'src'},
      zip_safe=False)