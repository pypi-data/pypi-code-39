import setuptools
import os

# supply contents of our README file as our package's long description
with open("README.md", "r") as fh:
    long_description = fh.read()

# gather all subdirs under "xtgen" as packages
packages = ["xtgen"]
for root, dirs, files in os.walk("xtgen/assets"):
    if len(files):
        root = root.replace("\\", ".")
        root = root.replace("/", ".")
        packages.append(root)

#print("packages=", packages)

setuptools.setup(
    # this is the name people will use to "pip install" the package
    name="xtgen",

    # this must be incremented every time we push an update to pypi
    version="0.0.10",

    author="Roland Fernandez",
    author_email="rfernand@microsoft.com",
    description="A cmdline tool for generating code to train ML models, using latest research datasets and architectures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rfernand2",

    # note: xtgen package should have a "__init__.py" file 
    packages = packages,   #   setuptools.find_packages(),

    # this will be copied to a directory on the PATH
    scripts=[
        'scripts/xtgen.bat', 
        'scripts/xtgen',
        'scripts/run_xtgen.py'
    ],

    # normally, only *.py files are included - this forces our TOML and ASSET files to be included
    package_data={'': ['*.toml', '*.md', '*.txt', '*.py']},

    include_package_data=True,   

    # the packages that our package is dependent on
    install_requires=[
        "numpy", 
        "arrow", 
        "toml"
    ],

    # used to identify the package to various searches
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)