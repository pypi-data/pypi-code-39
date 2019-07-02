from setuptools import setup, find_packages
setup(name='draco-xbrl',
      version='0.1',
      url='https://github.com/maxantonio/draco-xbrl',
      license='MIT',
      author='Antonio',
      author_email='max@irstrat.com',
      description='Parse xbrl files with mexican taxonomies',
      packages=find_packages(exclude=['ejemplo']),
      long_description=open('README.md').read(),
      zip_safe=False)