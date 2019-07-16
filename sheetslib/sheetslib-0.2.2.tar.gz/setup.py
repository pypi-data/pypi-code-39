import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='sheetslib',
    version='0.2.2',
    author="Casey Johnson",
    author_email="ctj0001@mix.wvu.edu",
    description="An object-oriented add-on for the gspread library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/caseyjohnsonwv/sheetslib",
    packages=['sheetslib'],
    include_package_data=True,
    install_requires = ['gspread'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
 )
