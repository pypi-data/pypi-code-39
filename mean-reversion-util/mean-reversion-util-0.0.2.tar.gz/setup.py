from setuptools import setup, find_packages


#import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup( 
    name="mean-reversion-util",
    version="0.0.2",
    description="Time Series mean reversion utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gjlr2000/johansen3.git",
    author="Gerardo Lemus",
    author_email="gerardo@alum.mit.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(),
    install_requires=[
          'scipy>=0.18.0',
          'statsmodels>=0.6.1',
          'numpy>=1.11.1',
          'pandas>=0.18.1',
          #'binance>=0.7.1',            
      ],
    include_package_data=True,

)