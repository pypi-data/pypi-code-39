import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="bryte",
    version="0.0.6",
    description="Python library of tools for enhancing your development, along with common shortcuts for speeding up your development",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mikeshobes718/Python-Packages",
    author="Mike Shobes",
    author_email="mikeshobes718@yahoo.com",
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["bryte"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "brytepython=bryte.__main__:main",
        ]
    },
)