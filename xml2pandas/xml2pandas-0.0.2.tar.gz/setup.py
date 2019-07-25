import os
from setuptools import find_packages, setup
# from io import open

with open(os.path.join(os.path.dirname(__file__), 'xml2pandas', 'readme.md'),  encoding='utf-8') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="xml2pandas",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",  # example license
    description="A simple Django app to compare numerical matrices simply",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/chasek23/xml2pandas",
    download_url='https://github.com/chasek23/xml2pandas/archive/0.0.0.tar.gz',
    author="Chase Kelly",
    author_email="chase@microsearch.net",
    install_requires=[
        'pandas',
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    project_urls={
        # 'Documentation': 'https://microsearch.cloud/',
        'Funding': 'https://microsearch.cloud/',
        'Say Thanks!': 'http://chasekel.ly/',
        'Source': 'https://github.com/chasek23/xml2pandas',
        'Tracker': 'https://github.com/chasek23/xml2pandas/issues',
    },
)
