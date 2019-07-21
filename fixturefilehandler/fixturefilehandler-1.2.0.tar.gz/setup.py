#!/usr/bin/env python
"""This module implements build settings."""
from setuptools import setup
from setuptools import find_packages


def main():
    """This function implements build settings."""
    with open('README.md', 'r', encoding='utf8') as file:
        readme = file.read()

    setup(
        name='fixturefilehandler',
        version='1.2.0',
        description=(
            'This project helps you to vacate specific file path '
            'or deploy resource file into specific file path when unit testing.'
        ),
        long_description=readme,
        long_description_content_type='text/markdown',
        author='Yukihiko Shinoda',
        author_email='yuk.hik.future@gmail.com',
        packages=find_packages(exclude=("tests*", "yourproduct*")),
        package_data={"fixturefilehandler": ["py.typed"]},
        python_requires='>3.6.0',
        install_requires=[],
        url="https://github.com/yukihiko-shinoda/fixture-file-handler",
        keywords="fixture file vacate deploy unittest pytest testing",
    )


if __name__ == '__main__':
    main()
