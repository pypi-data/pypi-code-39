# Heavily based of https://github.com/calebdinsmore/matillion-columns/blob/master/setup.py

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="es_xlsx2csv",
    version="0.0.8",
    author="Tory Harter",
    author_email="tory.harter@edusource.us",
    description="Command line tool to generate CSVs from XLSX files on S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tory-harter/xlsx2csv',
    license='MIT',
    entry_points={
        'console_scripts': ['es-xlsx2csv=es_xlsx2csv.command_line:main']
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'argparse',
        'boto3',
        'unicodecsv',
        'xlrd',
        'pandas',
        'openpyxl'

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
