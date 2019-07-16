from setuptools import setup, find_packages


long_description = open("README.rst", "r").read()


setup(
    name="arackpy",

    version="0.1",

    description="A multithreaded webcrawler and scraper",

    # display on pypi
    long_description=long_description,

    url="https://www.bitbucket.com/denisgomes/arackpy",

    author="Denis Gomes",

    author_email="denisg640@hotmail.com",

    license="BSD",

    # advertise program attributes
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        ],

    keywords="web crawler scraper",

    # excluded in build distributions, applies to packages only
    packages=find_packages(exclude=[
        "arackpy.docs", "arackpy.examples", "arackpy.tests"
        ]),

    # install from pypi, requirements.txt is for developers only
    install_requires=[],

    package_data={},

    # MANIFEST.in works for source distributions only
    data_files=[("", ["LICENSE.txt", "README.rst"])],

    # scripts= ,

    # tests
    test_suite="tests",

    )
