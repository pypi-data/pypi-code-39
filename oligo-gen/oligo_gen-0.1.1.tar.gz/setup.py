from setuptools import setup

setup(
	name='oligo_gen',
	version='0.1.1',
	description='generate oligos from fasta',
	py_modules=['oligo_gen'],
	package_dir={'':'oligo_gen'},
	install_requires=[
		'biopython',
	],
)
