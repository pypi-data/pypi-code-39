import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Eebuilder",
    version="0.5.0",
    author="Example Author",
    author_email="forsbergw82@gmail.com",
    description="A Python package for creating HTML files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
