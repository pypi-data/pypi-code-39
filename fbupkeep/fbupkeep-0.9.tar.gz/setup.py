#coding:utf-8
"""A setuptools based setup module for saturnin-sdk package.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
from codecs import open
from os import path
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='fbupkeep',
    version='0.9',
    description='Firebird Upkeep utility',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    url='https://github.com/pcisar/fbupkeep',
    author='Pavel Císař',
    author_email='pcisar@ibphoenix.cz',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',

        'Topic :: Database',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
        ],
    keywords='Firebird database backup maintenance',
    packages=find_packages(),  # Required
    zip_safe=False,
    install_requires=[],
    python_requires='>=3.5, <4',
    test_suite='nose.collector',
    data_files=[],
    namespace_packages=[],
    project_urls={
        'Source': 'https://github.com/pcisar/fbupkeep',
        },
    entry_points={'console_scripts': ['fbupkeep = fbupkeep.runner:main',
                                     ],
                  'fbupkeep_tasks': ['gstat = fbupkeep.tasks:TaskGstat',
                                     'sweep = fbupkeep.tasks:TaskSweep',
                                     'gbak = fbupkeep.tasks:TaskGbak',
                                     'gbak_restore = fbupkeep.tasks:TaskGbakRestore',
                                     'idx_recompute = fbupkeep.tasks:TaskIndexRecompute',
                                     'idx_rebuild = fbupkeep.tasks:TaskIndexRebuild',
                                     'remove_old = fbupkeep.tasks:TaskRemoveOld',
                                     ],
                 }
)
