from setuptools import setup, find_packages
 




setup(name='CubeStories',
      version='0.1',
      url='https://github.com/MaciejJanowski/CubeStories',
      license='MIT',
      author='Maciej Janowski',
      author_email='maciej.janowski@insight-centre.org',
      description='Data Story Pattern Analysis for LOSD',
      packages=find_packages(exclude=['tests']),
      install_requires=['SPARQLWrapper',
                        'sparql_dataframe','pandas',
                        'datastories',
                        'numpy','scipy'],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False)
