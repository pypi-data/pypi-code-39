import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="cusip_generator",
	version="0.0.3",
	author="Liu Chao",
	author_email="luis.liu.1018@gmail.com",
	description="Generate modified CUSIPs given Bloomberg Tickers",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/luisliuchao/cusip_generator",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)


# for new version

# 1. update the version
# 2. bundle to dist: python setup.py sdist bdist_wheel
# 3. upload to pypl: twine upload dist/*
