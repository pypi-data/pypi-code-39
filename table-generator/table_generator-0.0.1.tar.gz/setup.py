import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="table_generator",
    version="0.0.1",
    author="Arin Khare",
    author_email="arinmkhare@gmail.com",
    description="Generates code for html table from csv files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lol-cubes/table_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
    install_requires=[
        'lxml',
    ],
)