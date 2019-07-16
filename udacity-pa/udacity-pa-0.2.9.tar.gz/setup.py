from setuptools import setup

setup(
    name='udacity-pa',
    version='0.2.9',
    author='S. Charles Brubaker',
    author_email='cb@udacity.com',
    packages=['udacity_pa'],
    entry_points={
        'console_scripts': [
            'udacity = udacity_pa.projectassistant:main_func',
            'udacity_pa = udacity_pa.projectassistant:main_func'
        ],
    },
    include_package_data=True,
    url='http://github.com/udacity/udacity-pa',
    license='MIT',
    description="CLI tool for Udacity's project assistant.",
    keywords = 'Udacity',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "requests >= 2.2.1",
        "requests-toolbelt >= 0.7.0",
        "future"
    ],
)
