#!/usr/bin/env python3
import os

from setuptools import setup, find_packages


# Get long description about this python project.
with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setup(
    name='crlint',
    # TODO: remake package versioning.
    version=os.getenv('BITBUCKET_TAG') or os.environ['CT_LOCAL_VERSION'],
    python_requires='>=3.4',
    url='https://bitbucket.org/celadonteam/crtool',
    author='Celadon Developers',
    author_email='opensource@celadon.ae',
    description='The project copyright linter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    scripts=['crlint/__main__.py'],
    entry_points={
        'console_scripts': [
            'crlint=crlint.__main__:main',
        ],
    },
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development',
    ],
)
