from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='econmodels',
      version='0.1',
      description='A collection of econometric modelling tools',
      url='https://bitbucket.org/james_londal/econmodels/src/master/',
      author='James Londal',
      author_email='jameslondal@hearts-science.com',
      license='MIT',
      install_requires=[
         'pandas',
         'scipy',
         'scikit-learn',
         'matplotlib',
         'statsmodels',
      ],
      packages=['econmodels'],
      zip_safe=False)