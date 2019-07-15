#!/usr/bin/env python3


from setuptools import setup

from prodperfect import __author__, __email__, __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='django-prodperfect',
      version=__version__,
      description='Django template tags for ProdPerfect tracking snippet',
      long_description=long_description,
      long_description_content_type='text/markdown; charset=UTF-8',
      author=__author__,
      author_email=__email__,
      packages=['prodperfect', 'prodperfect.templatetags'],
      url='https://github.com/ProdPerfect/django-prodperfect',
      include_package_data=True,
      zip_safe=False,
      license='MIT',
      install_requires=[
          'django>=1.11'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Operating System :: OS Independent",
      ])
