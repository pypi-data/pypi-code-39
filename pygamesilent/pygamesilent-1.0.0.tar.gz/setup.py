"""  pygamesilent setup module.
Cribbed from: https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pygamesilent',
    version='1.0.0',
    description='Shim around PyGame to hide "Hello" message on import.',
    long_description=long_description,
    url='https://github.com/Julian-O/pygamesilent',
    author='Julian-O',
    author_email='pygamesilent@somethinkodd.com',
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: pygame',
    ],
    keywords='pygame shim',
    packages=['pygamesilent'],
    package_dir={'': 'src'},
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    install_requires=['pygame'],

    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['pytest', 'pytest-cov'],
    },

    project_urls={  # Optional
        'Source': 'https://github.com/Julian-O/pygamesilent/',
        'PyGame Info': 'https://pygame.org',
    },
)
