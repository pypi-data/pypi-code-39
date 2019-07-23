from setuptools import setup, find_packages
import os

setup(name="pymse",
      version="0.2",
      packages=find_packages(),
      include_package_data=True,
      description="Calculates multiscale entropy (MSE) of one or multiple data sets.",
      description_file="README.md",

      author="M. Costa",
      author_email="mcosta@fsa.harvard.edu",
      maintainer="Yeison Cardona",
      maintainer_email="yeison.eng@gmail.com",

      url="http://www.physionet.org/",
      download_url="https://bitbucket.org/yeisoneng/pymse/downloads",

      license="BSD 3-Clause",
      install_requires=["numpy"],

      keywords="mse",

      classifiers=[  # list of classifiers in https://pypi.python.org/pypi?:action=list_classifiers
                   "Programming Language :: Python",
      ],

      zip_safe=False

      )
