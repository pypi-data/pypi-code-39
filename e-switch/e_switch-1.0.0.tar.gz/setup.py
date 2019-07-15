from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='e_switch',
      version='1.0.0',
      description='hallo world this is my packaga for "e" tha packaga that switchas all "e"s with "a"s',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Safyre Lyons',
      author_email='lyons.safyre@gmail.com',
      license='MIT',
      py_modules=['e_switch'],
      package_dir={'': 'src'},
      zip_safe=False)