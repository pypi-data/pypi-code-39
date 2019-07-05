from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='timeql',
    version='0.0.0.dev',
    description='TimeQL programming language implemented in python',
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type='text/markdown',
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url='https://github.com/timeql/timeql',

    author='3demax',

    author_email='contact@timeql.org',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Interpreters',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='timeql language interpreter development',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.5, <4',

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    entry_points={
        'console_scripts': [
            'timeql=timeql:interpreter',
        ],
    },

    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    project_urls={
        'Bug Reports': 'https://github.com/timeql/timeql/issues',
        'Say Thanks!': 'https://saythanks.io/to/3demax',
    },
)
