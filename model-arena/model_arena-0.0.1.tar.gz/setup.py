import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="model_arena",
    version="0.0.1",
    author="Tansel Arif",
    author_email="tanselarif@live.co.uk",
    description="A model extension package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TanselArif-21/LinearRegression",
    packages=setuptools.find_packages(),
	install_requires=[
          'numpy',
          'pandas',
		  'sklearn',
		  'scipy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)