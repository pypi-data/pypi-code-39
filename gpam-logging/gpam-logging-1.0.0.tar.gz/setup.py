from setuptools import setup

version = '1.0.0'

setup(name='gpam-logging',
      version=version,
      description='Logger handler with GPAM integration',
      url='http://gpam.unb.br',
      author='GPAM',
      author_email='gpamunb@gmail.com',
      license='MIT',
      install_requires=[
      ],
      packages=[
          'gpam_logging',
      ],
      zip_safe=False)
