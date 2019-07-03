from setuptools import setup, find_packages

with open('VERSION.txt', 'r') as version_file:
    version = version_file.read().strip()

requires = ['']

setup(
    name='bbcu.rvcu',
    version=version,
    author='Refael Kohen',
    author_email='refael.kohen@weizmann.ac.il',
    packages=find_packages(),
    scripts=[
        'scripts/run-rvcu.py',
    ],
    description='Find RNA mutations and classify them by information form UMI (Unique Molecule Identifier)',
    long_description=open('README.txt').read(),
    install_requires=requires,
    tests_require=requires + ['nose'],
    include_package_data=True,
    test_suite='nose.collector',
)
