from setuptools import setup, find_packages

setup(
  name='libtado',
  version='0.0.1.dev1',
  author='Germain LEFEBVRE',
  author_email='germain.lefebvre4@gmail.com',
  description='A library (and a command line client) to control your Tado Smart Thermostat.',
  url='https://github.com/germainlefebvre4/libtado',
  license='GPLv3+',
  packages=find_packages(),
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
  ],
  install_requires=[
    'click',
    'requests'
  ],
  entry_points={
    'console_scripts': [
      'tado = libtado.__main__:main'
    ]
  }
)
