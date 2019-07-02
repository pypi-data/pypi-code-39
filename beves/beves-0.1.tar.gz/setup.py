import os
from os import path

from setuptools import setup, find_packages

from beves import metadata

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with open('requirements.txt') as requirement:
        for install in requirement:
            requirements_list.append(install.strip())

    return requirements_list


packages = find_packages(exclude=['tests*'])

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name=metadata.__program__,
      version=metadata.__version__,
      author=metadata.__author__,
      author_email='andremomorais@gmail.com',
      license='LGPLv3',
      url='https://github.com/andremmorais/beves',
      keywords='python telegram bot notification',
      description=metadata.__description__,
      test_suite='nose.collector',
      tests_require=['nose'],
      long_description_content_type='text/markdown',
      long_description=long_description,
      entry_points={
          'console_scripts': ['beves=beves.__main__:main'],
      },
      packages=packages,
      install_requires=requirements(),
      include_package_data=True,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Communications :: Chat',
          'Topic :: Internet',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'

      ],
      )
