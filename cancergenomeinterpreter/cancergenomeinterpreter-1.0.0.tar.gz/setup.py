from setuptools import setup, find_packages
from cancergenomeinterpreter import __version__, __author__, __email__

setup(
    name="cancergenomeinterpreter",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'pandas >= 0.22.0',
        'itab >= 0.9.0',
        'heapdict >= 1.0.0',
        'numpy >= 1.14.5',
        'TransVar >= 2.4.0.20180701',
        'humanize >= 0.5.1',
        'intervaltree',
        'pytabix'
    ],
    package_data={'': ['*.template', '*.template.spec']},
    author=__author__,
    author_email=__email__,
    description="Cancer Genome Interpreter",
    license="",
    keywords="",

    entry_points={
        'console_scripts': [
            'cgi = cancergenomeinterpreter.main:cmdline',
            'cgi-cna = cancergenomeinterpreter.cna.main:cmdline',
            'cgi-mut = cancergenomeinterpreter.mut.main:cmdline',
            'cgi-fus = cancergenomeinterpreter.fus.main:cmdline',
            'cgi-prescription = cancergenomeinterpreter.prescription.main:cmdline'
        ]
    }
)
