import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="semvercomp",
  version="0.1.0",
  author="Esteban Borai",
  author_email="estebanborai@outlook.com",
  description="Semantic Version Comparison for Python",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/estebanborai/semvercomp",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
