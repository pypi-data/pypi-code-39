#!/usr/bin/env python3


from pathlib import Path

from setuptools import setup

# Gets the long description from the README.md file
readme_filepath = Path(__file__).parent / 'README.md'
with readme_filepath.open('rt', encoding='utf-8') as fd_in:
    LONG_DESCRIPTION = fd_in.read()


setup(
    name='table-schema-resource-template',
    version='0.1.3',

    author='Christophe Benz',
    author_email='christophe.benz@jailbreak.paris',

    description="Generate a resource file template from a Table Schema JSON file",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    url="https://framagit.org/opendataschema/table-schema-resource-template",

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    packages=['table_schema_resource_template'],
    install_requires=[
        'iso8601',
        'tableschema >= 1.5.1',
        'xlsxwriter >= 1.1.8'
    ],

    entry_points={
        'console_scripts': [
            'table-schema-resource-template = table_schema_resource_template.cli:main',
        ],
    },
)
