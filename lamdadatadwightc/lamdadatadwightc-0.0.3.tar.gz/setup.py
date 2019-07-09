from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lamdadatadwightc",
    version="0.0.3",
    author="Dwight Churchill",
    author_email="dwight.a.churchill@gmail.com",
    description="Simple package to check nulls in your Pandas DataFrame and split datetimes into separate columns!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/dwightchurchill/lambdadwight/",
    download_url = 'https://github.com/dwightchurchill/lamdadatadwightc/dist/lamdadatadwightc-0.0.2.tar.gz',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)