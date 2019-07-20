import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyehub",
    version="1.3.1",
    author_email="revins@uvic.ca",
    description="A library used to solve an energy hub model in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/energyincities/pyehub",
    packages=setuptools.find_packages(exclude="pytests"),
    include_package_data=True,
    install_requires=[
        'pulp',
        'contexttimer',
        'pandas',
        'numpy',
        'PyYAML',
        'xlrd',
        'jsonschema',
        'pylint',
        'openpyxl',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)
