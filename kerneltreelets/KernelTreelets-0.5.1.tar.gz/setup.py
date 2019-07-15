import setuptools


with open("README.md", "r") as fh:
	long_description = fh.read()
	
setuptools.setup(
	name = "KernelTreelets",
	version = "0.5.1",
	author = "H. Xia",
	author_email = "hedixia@ucsb.edu",
	description = long_description,
	long_description = long_description,
	url = "https://github.com/hedixia/KernelTreelets_v5",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)