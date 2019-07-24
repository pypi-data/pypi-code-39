import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="bitfex",
  version="1.0.1",
  author="BitFex.Trade",
  author_email="support@bitfex.trade",
  description="BitFex.Trade python API wrapper",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/bitfex/bitfex_api.py",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires=[
    'requests'
  ]
)