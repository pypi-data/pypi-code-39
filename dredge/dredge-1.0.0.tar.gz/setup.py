from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'dredge',
  packages = ['dredge'],
  version = '1.0.0',
  description = 'User-friendly thresholded subspace-constrained mean shift for geospatial data',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = 'Ben Moews',
  author_email = 'ben.moews@protonmail.com',
  url = 'https://github.com/moews/dredge',
  keywords = ['density ridges',
              'spatial analysis',
              'principal curves',
              'route optimization',
              'hot spot analysis'],
  classifiers = ['Programming Language :: Python :: 3 :: Only',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License'],
  install_requires = ['numpy',
                      'scipy >= 0.18.1',
                      'schwimmbad >= 0.3.0',
                      'scikit-learn >= 0.19.1'],
)
