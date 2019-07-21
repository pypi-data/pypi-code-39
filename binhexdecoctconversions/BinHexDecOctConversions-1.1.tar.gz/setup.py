# Build and Upload
# 1) Navigate to 'C:\Users\Bob Phillips\Desktop\Alex\Python-Stuff\BinHexDecOctConversions'
# 2) Run 'python setup.py sdist bdist_wheel'
# 3) Run 'python -m twine upload dist/*'

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BinHexDecOctConversions",
    version="1.1",
    author="Timothy Bowen",
    author_email="tbowen2k@gmail.com",
    description="A package that converts between binary, hexadecimal, decimal and octal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TimothyBowen/BinHexDecOctConversions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)