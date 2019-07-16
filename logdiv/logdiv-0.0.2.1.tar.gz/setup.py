import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name='logdiv',
	version='0.0.2.1',
	author='Alexandre Wilmet',
	author_email='wilmet.alex@gmail.com',
	description='A package to mesure diversity of log files',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=setuptools.find_packages(),

	url="https://github.com/pedroramaciotti/diversity-patterns",
	classifiers=['Intended Audience :: Science/Research',
				 'Programming Language :: Python',
				 'Operating System :: Unix']
)
