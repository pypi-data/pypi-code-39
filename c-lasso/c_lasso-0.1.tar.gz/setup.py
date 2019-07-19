from setuptools import setup, find_packages

setup(name='c_lasso',
      version='0.1',
      license='MIT',
      author='Leo Simpson',
      url='https://github.com/Leo-Simpson/CLasso',
      author_email='leo.bill.simpson@gmail.com',
      description='Algorithms for constrained Lasso problems',
      packages=['classo'],
      long_description=open('README.md').read(),
      zip_safe=False)