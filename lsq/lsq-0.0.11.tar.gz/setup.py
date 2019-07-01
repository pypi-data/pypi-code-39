from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
	name = 'lsq',
	version = '0.0.11',
	description = 'Python Library to interact with Leadsquared API easily',
	long_description = long_description,
	long_description_content_type="text/markdown",
	url = 'https://github.com/seanjin17/lsq-python',
	author = 'Anand Sandilya',
	author_email = 'anand.sandilya@leadsquared.com',
	LICENSE = 'MIT',
	classifiers=[
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	keywords = 'leadsquared lsq lsqpython lsqpip',
	packages = find_packages(exclude = ['docs' , 'tests*']),
	install_requires = ['requests'],
	package_data = {
		'lsq' : ['package_data.dat']
	},
	data_files = None,
	extry_points = {
		'console_scripts' : [
			'help:lsq:help_console',
			],
		}
	)
#python3 setup.py sdist bdist_wheel
#python3 -m twine upload dist/*