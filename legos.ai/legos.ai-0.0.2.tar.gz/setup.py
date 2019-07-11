import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="legos.ai",
    version="0.0.2",
    description="A simple framework for fast protopying of Deep Learning researches.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/quanhua92/legos",
    author="Quan Hua",
    author_email="quanhua92@gmail.com",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
)