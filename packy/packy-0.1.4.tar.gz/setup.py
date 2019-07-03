from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='packy',  # Required
    version='0.1.4',
    description='Package manager for downloading packages ' \
                'from content providers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='codetent',
    url='https://github.com/codetent/packy',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='package CDNJS JS packet',
    py_modules=['packy'],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'packy=packy:main'
        ]
    },
)
