import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binary_tree",
    version="0.0.1",
    author="Ofri Kirshen",
    author_email="okirshen@gmail.com",
    description="Binary_tree is a simple package to create sort and search data with binary trees.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Okirshen/binary_tree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
