from setuptools import setup
import os
with open("README.md",'r') as f:
	long_description = f.read()
os.system("python -m pip install colorama")
setup(
	name='Enhanced PsExec',
	version='0.3.4',
	description='Enhanced PSEXEC',
	py_modules=["Epsexec"],
	package_dir={'': 'src'},

	long_description=long_description,
	long_description_content_type="text/markdown",

	url="https://github.com/orishamir/",
	author="Ori Shamir",
	author_email="Epsexecnoreply@gmail.com",

	classifiers=[
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.7",
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Topic :: System :: Systems Administration",
		"Operating System :: Microsoft :: Windows"
	]

	)