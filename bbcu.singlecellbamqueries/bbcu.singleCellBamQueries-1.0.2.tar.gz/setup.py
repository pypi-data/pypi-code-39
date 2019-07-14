from setuptools import setup, find_packages

with open('VERSION.txt', 'r') as version_file:
    version = version_file.read().strip()

requires = ['']

setup(
    name='bbcu.singleCellBamQueries',
    version=version,
    author='Refael Kohen',
    author_email='refael.kohen@weizmann.ac.il',
    packages=find_packages(),
    scripts=[
        'scripts/single-cell-bam-queries.py',
    ],
    description='Queries on bam file of single cell per genome position',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    install_requires=requires,
    tests_require=requires + ['nose'],
    include_package_data=True,
    test_suite='nose.collector',
)
